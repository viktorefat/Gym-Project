# Gym Strong

Gym Strong is a modern, responsive web application built with Python, Django, and Tailwind CSS designed for fitness centers and gyms. The platform enables users to browse and buy premium supplements, purchase gym memberships, manage personal profiles, and track shopping cart operations.

## Features

- **Supplements Shop:** Full product catalog featuring client-side Search, Autocomplete, and Live Suggestions built with high-performance Vanilla JavaScript.
- **Dynamic Shopping Cart:** Add products to your cart asynchronously using background AJAX / Fetch API queries with custom UI Toast feedback notifications.
- **Checkout System:** Form processing to finalize orders with local market validation (MKD currency) and automatic account membership activation.
- **Profile Management:** Personalized user profiles featuring avatar uploading, live image previewing, active subscription tier displays, and editable credentials.
- **Dual-Language Support (EN/MK):** Implemented via integrated Google Translate configurations, customized to set English (EN) as the default language while blocking default Google hover highlights and layout shifting elements.
- **Admin Management Panel:** Superusers can dynamically append new products, modify supplements directly from the modal view (with real-time data updates), and track current orders straight from the UI.
- **Cookie Compliance:** Custom aesthetic "Healthy Cookies" configuration banner utilizing browser local storage mechanisms.

---

## Tech Stack

- **Backend Framework:** Django (Python 3)
- **Frontend Styling:** Tailwind CSS, Google Fonts (Poppins)
- **Database:** SQLite (Default development)
- **Asynchronous Actions:** JavaScript (Vanilla Fetch API / AJAX)

---

## Getting Started

### Prerequisites

Ensure you have Python installed on your local machine.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/gym-strong.git](https://github.com/your-username/gym-strong.git)
   cd gym-strong
