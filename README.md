# HBnB - Technical Guide

## Introduction
Welcome to the **HBnB Technical Guide**. This document provides a comprehensive blueprint for implementing the HBnB platform, a web-based application designed to connect hosts offering accommodations with travelers seeking short-term rentals. Similar to established platforms like Airbnb, HBnB enables hosts to list properties, manage bookings, and communicate with guests, ensuring a seamless and secure booking experience.

This guide is intended for developers, system architects, and project managers. It outlines the core architecture, features, technical requirements, system components, and integration processes necessary for efficient development and deployment of the HBnB platform.

## Table of Contents
- [System Overview](#system-overview)
- [Technical Stack](#technical-stack)
- [System Architecture](#system-architecture)
- [Core Features](#core-features)
- [Database Design](#database-design)
- [API Design](#api-design)
- [User Authentication](#user-authentication)
- [Deployment Strategy](#deployment-strategy)
- [Security Considerations](#security-considerations)
- [Conclusion](#conclusion)

## System Overview
HBnB is designed as a scalable, full-stack web application that facilitates property rentals by connecting hosts and guests. The system consists of:
- A **frontend** for user interaction
- A **backend** managing business logic
- A **database** storing property, user, and booking data

## Technical Stack
- **Frontend**: HTML, CSS, JavaScript (React/Vue.js)
- **Backend**: Python (Flask/Django)
- **Database**: MySQL/PostgreSQL
- **Authentication**: OAuth, JWT
- **Deployment**: Docker, Nginx, AWS/GCP

## System Architecture
The system follows a **microservices-based** or **monolithic** architecture depending on scaling needs. Key components include:
- **Frontend UI** - User-friendly web interface
- **API Layer** - RESTful API for communication
- **Database** - Persistent data storage
- **Authentication Service** - Secure user authentication and authorization
- **Booking Engine** - Manages property reservations
- **Messaging Service** - Facilitates host-guest communication

## Core Features
- User Registration & Authentication
- Property Listing & Management
- Search & Filtering
- Booking & Payment Integration
- Review & Rating System
- Messaging System
- Admin Dashboard

## Database Design
The HBnB database follows a **relational model** with the following key tables:
- `users` (id, name, email, password, role)
- `properties` (id, owner_id, title, description, location, price)
- `bookings` (id, user_id, property_id, check-in, check-out, status)
- `reviews` (id, user_id, property_id, rating, comment)
- `messages` (id, sender_id, receiver_id, content, timestamp)

## API Design
HBnB exposes a RESTful API with endpoints for managing the platform:
```plaintext
GET /properties - Fetch available properties
POST /properties - Add a new property
GET /bookings - Retrieve user bookings
POST /bookings - Create a new booking
POST /auth/login - User authentication
```

## User Authentication
Authentication follows a **token-based** system using:
- **JWT (JSON Web Token)** for session management
- **OAuth 2.0** for third-party login (Google, Facebook)
- **Role-based Access Control (RBAC)** for admin, host, and guest privileges

## Deployment Strategy
HBnB is deployed using:
- **Docker & Docker Compose** for containerization
- **Nginx** for load balancing
- **AWS/GCP** for cloud hosting
- **CI/CD Pipelines** using GitHub Actions or Jenkins

## Security Considerations
To ensure a secure platform, HBnB implements:
- **Data encryption** (HTTPS/TLS)
- **Input validation & sanitization**
- **Secure password hashing** (bcrypt)
- **API rate limiting**

## Conclusion
By following this guide, developers can efficiently build and scale the HBnB platform, ensuring a robust, secure, and user-friendly experience. For additional documentation or questions, please refer to the project's GitHub repository or contact the development team.

## Authors:

**Alexis Battistoni** https://github.com/Albat93

**Killian Ripoche** https://github.com/KillianRipoche

**Jean-Alain Renié** https://github.com/JaRenie-spec

**Happy Coding! 🚀**

