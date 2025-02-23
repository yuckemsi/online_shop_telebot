# Telegram Bot for Product Management

This project is a Telegram bot designed to manage products, orders, reviews, and user support. The bot provides an admin panel for administrators to manage products and orders, and a user interface for customers to browse products, place orders, and leave reviews.

## Features

- **User Management**: Automatically adds new users to the database when they start the bot.
- **Product Management**: Allows administrators to add, delete, and view products.
- **Order Management**: Users can place orders, and administrators can view and manage these orders.
- **Review Management**: Users can leave reviews, and administrators can view them.
- **Support**: Users can ask questions, and administrators can respond to them.

## Setup

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Create a `config.py` file with your Telegram bot token:
    ```python
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    ```
4. Run the bot using `python main.py`.

## Usage

- **Start the Bot**: Users can start the bot by sending the `/start` command.
- **Browse Products**: Users can view available products.
- **Place Orders**: Users can place orders for products.
- **Leave Reviews**: Users can leave reviews for products.
- **Admin Panel**: Administrators can manage products and orders through the admin panel.

## Database

The bot uses SQLite for database management. The database schema includes tables for users, products, orders, reviews, and support questions.

## License

This project is licensed under the MIT License.