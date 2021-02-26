<!-- ABOUT THE PROJECT -->
# About The Project

![Postman Screen Shot](https://github.com/SedatOzdemir/usom-api-service/blob/main/images/USOM%20API.png?raw=true "Optional title")

The USOM API Service Tool that collecting phishing links and security announcements shared by USOM.gov.tr. Also  ​​to support over API.  It also allows the collected data to be share with API.

<!-- GETTING STARTED -->
## Getting Started

### Installation and Usage

1. Clone the repo
   ```sh
   git clone https://github.com/SedatOzdemir/usom-api-service
   ```
  
2. Run screen
   ```sh
   screen
   ```
3. Start api_service.py with Python3 (You can monitor that screen for API requests)
![API service screenshot](https://github.com/SedatOzdemir/usom-api-service/blob/main/images/API%20Service%20Screenshot.png?raw=true "Optional title")
   ```sh
   python3 api_service.py
   ```
4. Detach the screen with Ctrl + A + D keys.
5. Run screen
   ```sh
   screen
   ```
6. Start collector_service.py with Python3 (You can monitor that screen while tool collecting data)
![Collector service screenshot](https://github.com/SedatOzdemir/usom-api-service/blob/main/images/Collector%20Screenshot.png?raw=true "Optional title")
   ```sh
   python3 collector_service.py
   ```
7. Detach the screen with Ctrl + A + D keys

## API Usage
### Authorization

The API requests require the use of a generated AccessKey key. You can find your default AccessKey in config.ini file or generate a new one, by changing in configs.

To authenticate an API request, you should provide your API key in the 'access_token' parameter.

Example request:
```http
GET /api/usom?page=0&size=10&orderby=desc&data_type=malicious_links&access_token=178C4598781EF1D7F5193920D62FE0523445A6F4E911695FFB1400A0309F86A27924B0CE282589D56F8BEA8A088D61737DBEE043D710CCE66A20284F35B75042
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `access_token` | `string` | **Required**. Your access token |
| `page` | `int` | Page number for pagging |
| `size` | `int` | Row size per page |
| `data_type` | `string` | malicious_links or security_announcement |

### Responses

API endpoints return the JSON representation of the resources created or edited. However, if an invalid request is submitted, or some other error occurs, USOM API returns a JSON response in the following format:

```javascript
{
  "status" : string,
  "message" : string,
}
```

The `message` attribute contains a message commonly used to indicate errors or, in the case of deleting a resource, success that the resource was properly deleted.

The `status` attribute describes if the transaction was successful or not.

## Status Codes

API returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 401 | `UNAUTHORIZED` |
| 500 | `INTERNAL SERVER ERROR` |

## Examples
### cURL Request
```bash
curl --location --request GET 'http://127.0.0.1:5001/api/usom?page=0&size=10&orderby=desc&data_type=security_announcement&access_token=178C4598781EF1D7F5193920D62FE0523445A6F4E911695FFB1400A0309F86A27924B0CE282589D56F8BEA8A088D61737DBEE043D710CCE66A20284F35B75042'
```

### wGET Request

```bash
wget --no-check-certificate --quiet \
  --method GET \
  --timeout=0 \
  --header '' \
   'http://127.0.0.1:5001/api/usom?page=0&size=10&orderby=desc&data_type=security_announcement&access_token=178C4598781EF1D7F5193920D62FE0523445A6F4E911695FFB1400A0309F86A27924B0CE282589D56F8BEA8A088D61737DBEE043D710CCE66A20284F35B75042'
```
## Contact and help

Sedat Ozdemir - [Linkedin](https://www.linkedin.com/in/sedat0zdemir/) - sedat[dot]ozdemir[at]protonmail.com
Project Link: [https://github.com/SedatOzdemir/usom-api-service](https://github.com/SedatOzdemir/usom-api-service)
