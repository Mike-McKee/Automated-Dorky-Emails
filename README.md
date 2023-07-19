# Automating My Learning Process

Since I'm on a mission to conquer the **dorky world of data**, I'm learning all the time. As an experienced writer, I learn best when I write about what I learn. That's why I've created [Dorky Data.](https://www.dorkydata.com/)

It gives me a platform to write about what I learn and it serves as a repository/hub to store my knowledge. Pretty cool, huh?

Anyway, since I have so much to learn, I never know *what* to learn or review.

That's where this project comes in.

I'm automating my learning by creating a Python script that automatically sends me an email every morning with one of my blog posts for me to reread. Here's how I'm doing it:

1. Create a web scraper to find data regarding all my blog posts
2. Transport new data into a database (I'm using `MySQL` and `MongoDB`)
3. Write a script that accesses the databases and sends me a random link every morning