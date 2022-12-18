import networkx as nx
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Edge, Profile, Pairing


def make_pairings(request):
    for profile in Profile.objects.all():
        profile.has_tag_pairing = False
        profile.tag_pairing = None
        profile.tag_pairing2 = None
        profile.save()

    G = nx.Graph()

    # form the list of edges
    edge_list = []
    for edge in Edge.objects.all():
        profile1 = Profile.objects.get(user=edge.user1)
        profile2 = Profile.objects.get(user=edge.user2)
        if edge.active and profile1.active and profile2.active:
            edge_list.append((edge.user1.username, edge.user2.username, edge.weight))

    # I should add a function to check the integrity of the edges (ie. no repeats and confirm no strikes are matched)

    G.add_weighted_edges_from(edge_list)
    pairings = nx.max_weight_matching(G, maxcardinality=True)

    Pairing.objects.all().delete()
    for pair in pairings:
        user1 = User.objects.get(username=pair[0])
        user2 = User.objects.get(username=pair[1])
        profile1 = Profile.objects.get(user=user1)
        profile2 = Profile.objects.get(user=user2)

        Pairing.objects.create(user1=user1, user2=user2)

        if (user2 in profile1.strikes.all()) or (user1 in profile2.strikes.all()):
            print(
                "Two struck users were in the list of pairings. Please check and redo!"
            )
            return -1

        if profile1.has_tag_pairing == False and profile2.has_tag_pairing == False:
            profile1.has_tag_pairing = True
            profile1.save()

            profile2.has_tag_pairing = True
            profile2.save()

        if (user2 in profile1.strikes.all()) or (user1 in profile2.strikes.all()):
            return -1

    for profile3 in Profile.objects.filter(active=True):
        if profile3.user.is_superuser:
            continue
        if profile3.has_tag_pairing == False:
            for pair in Pairing.objects.all():
                user1 = pair.user1
                user2 = pair.user2
                user3 = profile3.user
                profile1 = Profile.objects.get(user=user1)
                profile2 = Profile.objects.get(user=user2)

                if (
                    (user1 not in profile2.strikes.all())
                    and (user1 not in profile3.strikes.all())
                    and (user2 not in profile1.strikes.all())
                    and (user2 not in profile3.strikes.all())
                    and (user3 not in profile1.strikes.all())
                    and (user3 not in profile2.strikes.all())
                ):
                    profile3.has_tag_pairing = True
                    pair.user3 = user3
                    pair.save()
                    profile3.save()
                    return 2

            messages.error(
                request,
                "For some reason we were unable to find a valid pairing for "
                + profile3.user.first_name
                + " "
                + profile3.user.last_name
                + ". They may have no valid pairings... Contact Kyle or try again.",
            )
            return -2

    return 1


def push_pairings(pairings, request):
    for profile in Profile.objects.all():
        profile.tag_pairing = None
        profile.tag_pairing2 = None

    for pair in pairings:
        if pair.user3 == None:
            user1 = pair.user1
            user2 = pair.user2
            profile1 = Profile.objects.get(user=user1)
            profile2 = Profile.objects.get(user=user2)

            if (user2 in profile1.strikes.all()) or (user1 in profile2.strikes.all()):
                print(
                    "Two struck users were in the list of pairings. Please check and redo!"
                )
                return -1

            profile1.tag_pairing = user2
            profile1.save()

            profile2.tag_pairing = user1
            profile2.save()

            for edge in user1.user1.filter(user2=user2):
                edge.weight = edge.weight / 10
                edge.save()
            for edge in user1.user2.filter(user1=user2):
                edge.weight = edge.weight / 10
                edge.save()

        else:
            user1 = pair.user1
            user2 = pair.user2
            user3 = pair.user3
            profile1 = Profile.objects.get(user=user1)
            profile2 = Profile.objects.get(user=user2)
            profile3 = Profile.objects.get(user=user3)

            if (
                (user1 in profile2.strikes.all())
                or (user1 in profile3.strikes.all())
                or (user2 in profile1.strikes.all())
                or (user2 in profile3.strikes.all())
                or (user3 in profile1.strikes.all())
                or (user3 in profile2.strikes.all())
            ):
                print(
                    "Two struck users were in the list of pairings. Please check and redo!"
                )
                return -1

            profile1.tag_pairing = user2
            profile1.tag_pairing2 = user3
            profile1.save()

            profile2.tag_pairing = user1
            profile2.tag_pairing2 = user3
            profile2.save()

            profile3.tag_pairing = user1
            profile3.tag_pairing2 = user2
            profile3.save()

            # user 1 to 2 edge
            for edge in user1.user1.filter(user2=user2):
                edge.weight = edge.weight / 10
                edge.save()
            for edge in user1.user2.filter(user1=user2):
                edge.weight = edge.weight / 10
                edge.save()

            # user 1 to 3 edge
            for edge in user1.user1.filter(user2=user3):
                edge.weight = edge.weight / 10
                edge.save()
            for edge in user1.user2.filter(user1=user3):
                edge.weight = edge.weight / 10
                edge.save()

            # user 2 to 3 edge
            for edge in user2.user1.filter(user2=user3):
                edge.weight = edge.weight / 10
                edge.save()
            for edge in user2.user2.filter(user1=user3):
                edge.weight = edge.weight / 10
                edge.save()

    for profile in Profile.objects.filter(active=True):
        if profile.user.is_superuser:
            continue
        if profile.has_tag_pairing == False:
            messages.error(
                request,
                "For some reason we were unable to find a valid pairing for "
                + profile.user.first_name
                + " "
                + profile.user.last_name
                + " and they were left unpaired. :(",
            )
            return -4
        if profile.tag_pairing in profile.strikes.all():
            return -2
        if profile.tag_pairing2 != None:
            if profile.tag_pairing2 in profile.strikes.all():
                return -2

    return 1


def clear_pairings():
    Pairing.objects.all().delete()
    for profile in Profile.objects.all():
        profile.tag_pairing = None
        profile.tag_pairing2 = None
        profile.save()


def create_edges(user1, user2, active=True, weight=100.0):
    if user1 == user2:
        print("Edge can not be made to yourself")
        return

    for edge in user1.user1.all():
        if edge.user2 == user2:
            print(
                f"Edge btwn {user1.username} and {user2.username} already exists with weight {edge.weight}. Active = {edge.active}"
            )
            return

    for edge in user1.user2.all():
        if edge.user1 == user2:
            print(
                f"Edge btwn {user1.username} and {user2.username} already exists with weight {edge.weight}. Active = {edge.active}"
            )
            return

    if user1.is_superuser or user2.is_superuser:
        print("Edge can not be made with a superuser")
        return

    Edge.objects.create(user1=user1, user2=user2, active=active, weight=weight)


def populate_edges(newuser):
    for olduser in User.objects.all():
        if olduser.is_superuser:
            continue
        if olduser != newuser:
            profile = Profile.objects.get(user=olduser)
            create_edges(user1=olduser, user2=newuser, active=profile.active)
