# http_client.py
import requests

def main():
    url = "https://httpbin.org/get"
    post_url = "https://httpbin.org/post"

    try:
        # GET request
        print("\n--- GET Request ---")
        response = requests.get(url)
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Body:", response.text[:200], "...")  # print first 200 chars

        # POST request
        print("\n--- POST Request ---")
        data = {"name": "Ravindra", "msg": "Hello from HTTP client"}
        response = requests.post(post_url, data=data)
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Body:", response.text[:200], "...")

    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    main()
