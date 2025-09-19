# Simple HTTP Server

## Overview
This is a **basic HTTP server** written in Python.  
It serves static HTML/CSS files from the `www/` directory and handles `404 Not Found` errors with a funny error page.

---

## Project Structure

```
simple_http_server/
│
├── server.py          # Python HTTP server
└── www/               # Website files
    ├── index.html     # Home page
    ├── about.html     # About page
    ├── 404.html       # Custom 404 error page
    ├── index.css      # Styles for index.html
    ├── about.css      # Styles for about.html
    └── 404.css        # Styles for 404.html
```

---

## How to Run

1. Open a terminal and navigate to the project folder:
   ```bash
   cd Lab\ 1/simple_http_server
   ```

2. Start the server:
   ```bash
   python3 server.py
   ```

3. Open your browser and go to:
   ```
   http://127.0.0.1:8080/
   ```

---

## Pages

- **Home** → `http://127.0.0.1:8080/`  
  Funny welcome message + bouncing pill navbar

- **About** → `http://127.0.0.1:8080/about.html`  
  About page with its own funny text

- **404** → `http://127.0.0.1:8080/404.html`  
  Flashing red background + shaking navbar, with a silly message

---

## Features

- Serves `.html` and `.css` files
- Funny custom messages on each page
- Animated navigation bar ("pill")
- Custom 404 error page that flashes red and shakes
