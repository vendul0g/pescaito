import requests

def check_main_page(url):
    results = {
        "status_code_404": False,
        "body_contains_404_message": False,
        "headers_contain_content_type_plain": False,
        "headers_contain_x_content_type_options_nosniff": False,
        "headers_contain_vary_accept_encoding": False
    }

    try:
        response = requests.get(url)
        
        # Check if status code is 404
        if response.status_code == 404:
            results["status_code_404"] = True
        
        # Check if body contains "404 page not found"
        if "404 page not found" in response.text:
            results["body_contains_404_message"] = True
        
        # Check for specific headers
        headers = response.headers
        if headers.get("Content-Type") == "text/plain; charset=utf-8":
            results["headers_contain_content_type_plain"] = True
        if headers.get("X-Content-Type-Options") == "nosniff":
            results["headers_contain_x_content_type_options_nosniff"] = True
        if "Vary" in headers and "Accept-Encoding" in headers["Vary"]:
            results["headers_contain_vary_accept_encoding"] = True

    except requests.RequestException as e:
        print(f"Error fetching the main page: {e}")

    return results

def check_robots_txt(url):
    robots_url = url.rstrip('/') + "/robots.txt"
    try:
        response = requests.get(robots_url)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return False

def check_gophish(url: str) -> int:
    # Inicializamos el contador
    counter = 0

    # Hacemos las comprobaciones
    main_page_results = check_main_page(url)
    robots_txt_accessible = check_robots_txt(url)

    # Vemos los resultados
    print("Main Page Check Results:")
    for key, value in main_page_results.items():
        print(f"{key}: {value}")
        if value:
            counter += 1
    print(f"Robots.txt accessible: {robots_txt_accessible}")
    
    # Devolvemos el contador
    return counter

# Example usage
url = "https://iegitec.com"
print(f"Counter checks = {check_gophish(url)}")
