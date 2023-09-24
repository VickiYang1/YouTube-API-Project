import pandas as pd
import os


# Method to convert the video category id to category names
def get_video_categories(youtube):
    categories = {}
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()

    for item in response['items']:
        category_id = item['id']
        category_name = item['snippet']['title']
        categories[category_id] = category_name

    return categories


# method for displaying the top 50 trending videos on YouTube
def get_trending(youtube,region_code):
    all_data = []
    category_mapping = get_video_categories(youtube)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,id",
        chart="mostPopular",
        maxResults=50,
        regionCode=region_code

    )
    response = request.execute()

    for item in response['items']:
        data = {
            "Channel Name": item["snippet"]["channelTitle"],
            "Video Title": item["snippet"]["title"],
            "Views": item["statistics"]["viewCount"],
            "Video ID": item["id"],
            "Categories": category_mapping.get(item["snippet"]["categoryId"], "Unknown")
        }
        all_data.append(data)

    return pd.DataFrame(all_data)


# method to add more data to the csv file
def add_to_file(result,region_code):
    file_path = f"trending_videos{region_code}.csv"
    if not os.path.exists(file_path):
        # Creating an initial csv file for the trending videos
        columns = ["Channel Name", "Video Title", "Views", "Video ID", "Categories"]
        df = pd.DataFrame(columns=columns)

        df.to_csv(f"trending_videos{region_code}.csv", index=False)
        result.to_csv(f"trending_videos{region_code}.csv", index=False)
        return result

    existing_data = pd.read_csv(f"trending_videos{region_code}.csv")
    updated_data = pd.concat([result, existing_data], ignore_index =True)
    updated_data.drop_duplicates(subset=["Video ID"], inplace=True)

    updated_data.to_csv(f"trending_videos{region_code}.csv",index = False)

    print("Data successfully added to file")
    return updated_data


# method to search a specific youtube channel using their channel id
def search_channel(youtube, channel_id):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    )
    response = request.execute()

    for item in response['items']:
        data = {
            "Channel Name": item["snippet"]["title"],
            "Description": item["snippet"]["description"],
            "Subscribers": item["statistics"]["subscriberCount"],
            "Views": item["statistics"]["viewCount"],
            "Total Videos": item["statistics"]["videoCount"],
            "Playlist ID": item["contentDetails"]["relatedPlaylists"]["uploads"]
        }
        all_data.append(data)

    return pd.DataFrame(all_data)


# method to view a specific video's information from the trending section
def view_video(youtube,video_id):
    all_data = []
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    for video in response["items"]:
        stats_to_keep = {"snippet": ["channelTitle", "title", "description", "tags","publishedAt"],
                         "statistics":["viewCount", "likeCount", "commentCount"],
                         "contentDetails": ["duration"]}
        video_info={}

        video_info["video_id"] = video["id"]
        for i in stats_to_keep.keys():
            for j in stats_to_keep[i]:
                try:
                    video_info[j] = video[i][j]
                except:
                    video_info[j] = None
        all_data.append(video_info)
    return pd.DataFrame(all_data)


def display_category(category,region_code):
    df = pd.read_csv(f"trending_videos{region_code}.csv")
    condition = df["Categories"] == category
    filtered_df = df[condition]
    return filtered_df



