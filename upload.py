# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/code-samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload
# 3. The videos uploaded aare private and blocked. I need your help, youtube

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from oauth2client.tools import argparser
from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main(args):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # client_secrets_file
    client_secrets_file = args.secrets

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Upload video
    upload_request = youtube.videos().insert(
        
        body={
            "snippet": {
                "categoryId": "",
                "title": args.title,
                "description": args.description,
                "tags": [
                    "Cats",
                    "Kittens"
                ],
                "channelTitle": "Yoga Pets"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False 


            }
        },
        part="snippet,status",
        media_body=MediaFileUpload(args.file)
    )

    upload_response = upload_request.execute()
    video_id = upload_response["id"]
    print(f"Video uploaded. ID: {video_id}")

    # # Add video to playlist
    # playlist_id = "PL7QZhJ9HueoLE2bqjnObFOXrCKgrPF6Gg"
    # playlist_item_request = youtube.playlistItems().insert(
    #     part="snippet",
    #     body={
    #         "snippet": {
    #             "playlistId": playlist_id,
    #             "resourceId": {
    #                 "kind": "youtube#video",
    #                 "videoId": video_id
    #             }
    #         }
    #     }
    # )

    # playlist_item_response = playlist_item_request.execute()
    # print(f"Video added to playlist. Playlist Item ID: {playlist_item_response['id']}")

if __name__ == "__main__":
    argparser.add_argument("--file", required=True, help="Video file to upload")
    argparser.add_argument("--secrets", required=True, help="Video secrets", default="Default secrets")
    argparser.add_argument("--title", help="Video title", default="Test Title")
    argparser.add_argument("--description", help="Video description", default="Test Description")

    args = argparser.parse_args()

    if not os.path.exists(args.file):
        exit("Please specify a valid file using the --file= parameter.")
        
    main(args)
    
