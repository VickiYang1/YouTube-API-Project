from googleapiclient.discovery import build
import pandas as pd

from tabulate import tabulate
from OptionMethods import get_trending, view_video, search_channel, add_to_file, display_category
from Graph_Options import graph_all
import sys

# Get credentials and create an API client
api_key = "AIzaSyCqn35zzfBYi5pKQNLsJfL9IImz9Y3p-S4"
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)


def playlist_format(result):
    formatted_result = tabulate(result, headers='keys', showindex=range(1, len(result) + 1), tablefmt='pretty',
                                numalign="left", stralign="left")
    print(formatted_result)


def video_format(result):
    formatted_result = tabulate(result, headers='keys', showindex='never', tablefmt='pretty',
                                numalign="left", stralign="left")
    print(formatted_result)


def exit():
    print("Quitting program now, Thank You")
    sys.exit()


# method for displaying the user options
def selection():
    region_code = None
    result = pd.DataFrame()
    option = input("\nOptions Menu:\n----------------\n-View Trending (T)\n-Search Channel (S)\n-Display Graphs(D)\n-Quit (Q)\n")

    while (option.upper() != "Q"):

        if option.upper() == "T":
            next = input("\nSelect an Option:\n------------------\n-View all Trending Videos(T)\n-View Region Trending Videos(R)\n-Go Back(B)\n")
            if next.upper() == "T":
                region_code = "US"
                result = get_trending(youtube,region_code)
                playlist_format(result)
                next = input("\nSelect an Option:\n------------------\n-Add to File(F)\n-View A Trending Video(V)\n-View A Trending Category(C)\n-Go Back(B)\n")

            elif next.upper() == "R":
                region_code = input("Please input a 2 letter region code:\n").upper()
                result = get_trending(youtube, region_code)
                playlist_format(result)
                next = input("\nSelect an Option:\n------------------\n-Add to File(F)\n-View A Trending Video(V)\n-View A Trending Category(C)\n-Go Back(B)\n")

            if next.upper() == "C":
                category = input("Please enter the name of a category:\n").capitalize()
                result = display_category(category,region_code)
                playlist_format(result)
                next = input("\nSelect an Option:\n------------------\n-View A Trending Video(V)\n-Go Back(B)\n")

            if next.upper() == "F":
                result = get_trending(youtube,region_code)
                add_to_file(result, region_code)

            if next.upper() == "V":
                video_num = int(input("Please enter the index number of the video you would like to view:\n"))
                if 0 < video_num < len(result):
                    selected_video = result.iloc[video_num-1]
                    video_id = selected_video["Video ID"]
                    result = view_video(youtube, video_id)
                    video_format(result)
                else:
                    invalid_option()

            elif next.upper() == "B":
                selection()
            if next.upper() not in ["B", "V", "F", "C", "T"]:
                invalid_option()

        elif option.upper() == "S":
            channel_id = input("Enter a channelID:\n")
            result=search_channel(youtube, channel_id)
            video_format(result)

        elif option.upper() == "D":
            next = input(("\nSelect an Option:\n------------------\n-Display All Trending(A)\n-Display Trending Region Categories (R)\n"))
            if next.upper() == "A":
                region_code="us"
                graph_all(region_code)
            elif next.upper() == "R":
                region_code= input("Please enter a 2 letter region code:\n")
                graph_all(region_code)


        else:
            invalid_option()

        another_selection()

    exit()


def invalid_option():
    print("Please select a valid option")
    selection()


def another_selection():
    repeat = input("Would you like to make another selection? (Y/N):\n")
    if repeat.upper() == "Y":
        selection()
    elif repeat.upper() == "N":
        exit()
    else:
        print("Please select a valid option\n")
        another_selection()


def main():
    print("\nWelcome to the YouTube data analysis project! Please select an option:")
    selection()

main()

