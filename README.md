# 🏫 MOE Operations Portal

A comprehensive, multi-module Streamlit web application designed to digitize and streamline school operations. This platform consolidates transport logistics, co-curricular activity (CCA) management, and procurement into a single, unified workflow with role-based access and centralized oversight.

## ✨ Key Features

The portal is divided into four distinct mini-applications accessible via a unified sidebar:

### 🚌 1. Transport Services Module
* **Master Contract Management:** Upload annual vendor contracts to lock in negotiated rates.
* **Streamlined Dispatch:** Schools can instantly book buses directly with the contracted vendor.
* **Vendor Dashboard:** Mandated vendors acknowledge assigned jobs and provide driver/vehicle details.
* **Reconciliation:** Event-day trip completion tracking and automated monthly billing calculation.

### ⚽ 2. CCA Instructor Management
* **Contract Integration:** Upload master agreements for external sports and academic instructors.
* **Session Booking & Acceptance:** Teachers book specific hours; instructors review and accept sessions.
* **Event-Day Attendance:** Instructors log student attendance directly into the portal.
* **Automated Invoicing:** End-of-month consolidated reports calculate total payable hours based on contracted rates.

### 📦 3. Goods & Services Procurement
* **Purchase Orders:** Issue POs directly to pre-approved suppliers.
* **Supplier Portal:** Vendors update the system when goods or services are delivered.
* **Goods Receipt & Rating:** Schools verify deliveries, provide quality ratings, and authorize payments in a seamless 3-step pipeline.

### 👑 4. Master Admin Dashboard
* **Global Oversight:** A password-protected "God View" (`Password: EduTransit2026!`) for top-level administrators.
* **Cross-Module Metrics:** Real-time tracking of total bus trips, CCA sessions, and goods ordered.
* **Data Export:** View and export raw dataframes for every module.
* **System Controls:** Developer tools to clear and reset system data.

## 🛠️ Tech Stack

* **Frontend & Backend Logic:** [Streamlit](https://streamlit.io/) (Python)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Date/Time Handling:** Native Python `datetime`
* **Styling:** Custom GovTech/Public Sector Innovation UI via Streamlit theming.

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/moe-operations-portal.git](https://github.com/yourusername/moe-operations-portal.git)
   cd moe-operations-portal
