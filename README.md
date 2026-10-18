Copy the content below directly into your `README.md` file. It is formatted in standard Markdown.

Writing

# 📦 Moti Packaging Industries Pvt. Ltd. — AI-Powered Packaging Enquiry Management System

An AI-powered packaging enquiry management system built with **Python, Groq LLM, LangChain, Pydantic, SQLite, and Streamlit**.

The project automates customer enquiry processing, extracts structured lead information, splits enquiries by product application, identifies missing information, flags dimension-based approval requirements, generates follow-up emails, and provides an interactive dashboard for enquiry analysis.

It also includes an AI-powered LinkedIn post generator to create product marketing content and publish approved posts with product images.

## 🚀 Features

### 1\. AI-Powered Customer Enquiry Processing

- Processes customer enquiries written in natural language.
- Extracts structured customer and packaging information using a Groq-hosted LLM.
- Uses LangChain structured output and Pydantic validation.
- Applies strict extraction instructions to minimize guessed or fabricated information.
- Represents missing information as `None` wherever permitted by the schema.
- Preserves the original customer enquiry for reference.

### 2\. Product-Specific Enquiry Splitting

Automatically separates a single customer message into individual product-specific enquiries.

- Generates one enquiry for each distinct product being packed.
- Preserves customer and company details across relevant enquiries.
- Associates quantities, variant counts, accessories, and deadlines with the correct product.
- Preserves explicitly stated quantities without multiplying them by variant counts.
- Retains ambiguous quantities instead of silently resolving them.
- Avoids creating separate enquiries for accessories that belong to existing product requirements.

### 3\. Structured Lead Information Extraction

The system extracts the following fields:

| Field | Description |
| --- | --- |
| Customer Name | Customer's explicitly stated name |
| Company Name | Customer's company name |
| Mobile Number | Explicitly provided phone number |
| Email | Customer's email address |
| Product Application | Product intended to be packed |
| Product Category | Packaging category |
| Diameter | Diameter in millimetres |
| Height | Height in millimetres |
| Quantity | Explicit order quantity |
| Printing Details | Printing requirements |
| Delivery Location | Explicit delivery location |
| Required Date | Requested delivery date |
| Enquiry Status | Enquiry classification |

**Supported packaging categories:**

- Composite Cans
- Paper Tubes
- Industrial Packaging
- Caps, Lids & Closures
- TIN Cans

### 4\. Strict Extraction and Validation

The system uses a Pydantic model and structured output to enforce the expected data schema.

Extraction rules include:

- Extract only information supported by the customer message.
- Do not infer customer details from company names or other fields.
- Convert dimensions to millimetres only when the original units are clear.
- Do not confuse diameter with radius, width, or circumference.
- Extract an explicitly stated total quantity when unambiguous.
- Do not multiply quantities by the number of variants.
- Preserve a stated delivery date without inventing a missing year.
- Do not invent printing requirements, delivery locations, or contact details.

> **Note:** Prompting and schema validation reduce extraction errors but cannot guarantee that an LLM will never hallucinate. Production deployments should also use deterministic validation, source-text verification, and human review.

### 5\. Enquiry Classification

Each enquiry is assigned one of the following statuses:

| Status | Purpose |
| --- | --- |
| `ready to quotation` | Enquiry meets configured quotation requirements |
| `more information required` | Information is missing or readiness cannot be established |
| `not currently serviceable` | A configured business rule indicates that the enquiry cannot be processed |
| `possible duplicate enquiry` | Existing records provide evidence of a potential duplicate |

The classification is designed to avoid unsupported conclusions. Quotation requirements and duplicate detection should be implemented using explicit business rules and database checks.

### 6\. Dimension-Based Human Approval

The system checks product dimensions against configured business thresholds.

- Maximum diameter threshold: **2000 mm**
- Maximum height threshold: **5000 mm**

If either dimension exceeds its threshold, the application requests human approval before attempting to save the lead.

The reviewer can approve or reject the insertion.

### 7\. SQLite Database

The application uses SQLite to store extracted customer enquiries.

Stored information includes:

- Customer and company details
- Contact information
- Product application and category
- Dimensions and quantity
- Printing requirements
- Delivery location and date
- Enquiry classification
- Original customer message

The application uses parameterized SQL statements and `INSERT OR IGNORE` for database insertion.

A uniqueness constraint is configured on the combination of mobile number, product application, and height to help prevent certain duplicate records.

### 8\. AI-Generated Follow-Up Emails

Generates professional customer follow-up emails using extracted lead information.

The workflow can:

- Thank the customer for the enquiry.
- Summarize available customer and packaging details.
- List missing required information.
- Request confirmation of extracted information.
- Explain dimension-related restrictions when applicable.
- Request corrected dimensions if measurements may be incorrect.
- Avoid promising quotations, prices, production dates, or delivery dates without confirmation.

The email is displayed for human review before sending.

Available actions:

1. Approve and send the email.
2. Edit the email before sending.
3. Reject the email without sending.

Email delivery uses Gmail SMTP with credentials supplied through environment variables.

### 9\. Streamlit Enquiry Dashboard

The Streamlit dashboard provides an interactive overview of stored enquiries.

Features include:

- Total enquiry count
- Ready-for-quotation count
- Possible duplicate count
- Not-serviceable count
- Missing-information count
- Enquiries by packaging category
- Enquiry status distribution
- Search by customer, company, mobile number, or email
- Filter by packaging category and enquiry status
- Tabular enquiry records
- CSV export of filtered records
- Manual dashboard refresh

### 10\. AI-Powered LinkedIn Post Generator

The application includes a product marketing workflow for LinkedIn.

Features include:

- Product name input
- Product details and writing instructions
- AI-generated marketing copy
- Editable LinkedIn post content
- Product image upload and preview
- Optional product URL
- Explicit approval before publication
- LinkedIn image upload and post publishing through the LinkedIn API

The generation prompt instructs the model to use supplied product information and avoid inventing specifications, features, or certifications.

Generated marketing content should be reviewed for factual accuracy before publication.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Core application logic |
| Groq API | Language model inference |
| `openai/gpt-oss-120b` | Configured LLM |
| LangChain | LLM integration and structured output |
| Pydantic | Schema definition and field validation |
| SQLite | Lead data persistence |
| Streamlit | Interactive dashboard and LinkedIn interface |
| Pandas | Data loading, filtering, and tabular processing |
| Plotly Express | Dashboard visualizations |
| Requests | LinkedIn API requests |
| `smtplib` | Email delivery |
| `python-dotenv` | Environment variable management |
| Python Logging | Application logging and error tracking |

## 📁 Project Structure

Recommended project structure:

```
moti-packaging-enquiry-system/
│
├── assignmentf.py             # Enquiry processing and email workflow
├── dashboard.py               # Streamlit dashboard and LinkedIn tools
├── LeadData2.db               # Database used by the enquiry workflow and the dashboard
├── workflow.log               # Application logs
├── .env                       # Local environment variables
├── .gitignore                 # Files excluded from version control
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

The filenames above reflect the current implementation's separate database paths. Adjust the structure to match the actual files in your repository.

## ⚙️ Prerequisites

Before running the project, ensure you have:

- Python 3.10 or a compatible version supported by your installed dependencies.
- A Groq API key.
- Gmail SMTP credentials, including an app password if required.
- A LinkedIn developer application with the necessary API access and permissions if publishing posts.
- A LinkedIn member identifier and access token for the intended publishing account.

## 📥 Installation

### 1\. Clone the Repository

```
git clone <YOUR_REPOSITORY_URL>
cd moti-packaging-enquiry-system
```

Replace `<YOUR_REPOSITORY_URL>` with your repository URL.

### 2\. Create a Virtual Environment

```
python -m venv .venv
```

Activate the environment.

**Windows:**

```
.venv\Scripts\activate
```

**Linux/macOS:**

```
source .venv/bin/activate
```

### 3\. Install Dependencies

Create a `requirements.txt` file containing:

```
langchain-groq
pydantic
python-dotenv
pandas
plotly
streamlit
requests
```

Install the dependencies:

```
pip install -r requirements.txt
```

Pin and test compatible dependency versions before deploying the application.

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

SENDER_EMAIL=your_email@gmail.com
SENDER_APP_PASSWORD=your_gmail_app_password
```

Replace the example values with your actual credentials.

**Security recommendations:**

- Never commit `.env` to version control.
- Never hardcode API keys, email passwords, or access tokens.
- Use Gmail app passwords where applicable instead of your normal account password.
- Rotate exposed credentials immediately.
- Store production secrets in an appropriate secret manager.

## 🔗 LinkedIn API Configuration

The LinkedIn publishing feature reads credentials from Streamlit secrets.

Create `.streamlit/secrets.toml`:

```
[linkedin]
access_token = "YOUR_LINKEDIN_ACCESS_TOKEN"
api_version = "YOUR_SUPPORTED_LINKEDIN_API_VERSION"
member_id = "YOUR_LINKEDIN_MEMBER_ID"
```

Replace the placeholders with valid credentials and a supported API version.

The LinkedIn application must have the appropriate permissions for image uploads and publishing posts. Access tokens can expire or lose authorization, so configure renewal and error handling as appropriate.

**Important:** Do not commit `secrets.toml` to a public repository.

## ▶️ Running the Application

### 1\. Run the Enquiry Processing Workflow

```
python assignmet.py
```

The workflow processes the configured customer message and attempts to:

1. Split the message into product-specific enquiries.
2. Extract structured lead information.
3. Validate extracted fields against the Pydantic schema.
4. Determine the enquiry classification.
5. Request human approval when configured dimension thresholds are exceeded.
6. Insert eligible leads into the SQLite database.
7. Generate a follow-up email.
8. Display the email for review and request approval before sending.

The current script uses a sample customer message in the source code. Replace it with your input mechanism or connect it to an appropriate customer enquiry source.

### 2\. Run the Streamlit Dashboard

```
streamlit run dashboard.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

Users can review enquiries, filter records, export CSV data, generate LinkedIn content, upload product images, and publish approved posts.

## \

## 📊 Dashboard Metrics

The dashboard calculates enquiry counts from the `query_category` column and provides visualizations for:

- Enquiries by packaging category
- Enquiry status distribution
- Total stored enquiries
- Leads ready for quotation
- Potential duplicates
- Enquiries marked not serviceable
- Enquiries requiring additional information

The dashboard supports filtering and CSV export to help users review and analyze stored enquiries.

## 🛡️ Data Accuracy and Reliability

The project is designed to minimize unsupported data extraction, but an LLM alone cannot guarantee perfect accuracy.

Recommended safeguards include:

- Validate phone numbers, email addresses, dates, dimensions, and quantities independently.
- Preserve the original message alongside extracted values.
- Verify extracted fields against their supporting source text.
- Require human review for ambiguous or high-impact fields.
- Use deterministic code for business rules and dimension thresholds.
- Implement database-backed duplicate checks before assigning duplicate status.
- Keep the schema, SQL statements, and dashboard column names consistent.
- Test product splitting with messages containing multiple products and quantities.
- Avoid allowing model output to determine approvals without independent checks.

## ⚠️ Current Implementation Notes

Review the following items before using the project in production:

1. **Database consistency:** The workflow and dashboard currently reference different database files.
2. **SQL insertion:** Ensure every `INSERT` statement uses the exact schema column names. The human-approved insertion statement currently contains an incorrect column name and a trailing comma in its column list.
3. **Failure handling:** If LLM extraction fails, stop processing that enquiry before accessing extracted fields.
4. **Quantity handling:** Test product splitting and quantity extraction against ambiguous totals and accessory-specific quantities.
5. **Date handling:** The extraction prompt contains conflicting instructions about defaulting a missing year to 2026. Remove the default-year rule if missing years must never be inferred.
6. **Approval logic:** The dimension approval decision and `query_cat` classification should use consistent, independently implemented business rules.
7. **Email safety:** Validate the recipient address and retain explicit human approval before sending.
8. **LinkedIn publishing:** Confirm that the configured API version, token, permissions, and publishing endpoint are supported by your LinkedIn application.
9. **Duplicate detection:** `INSERT OR IGNORE` only handles conflicts covered by database constraints. It does not independently determine whether an enquiry is a duplicate.
10. **Logging and privacy:** Avoid logging sensitive customer information, credentials, or complete message contents unnecessarily.

## 🔮 Future Enhancements

Potential improvements include:

- A Streamlit form for entering customer enquiries directly.
- Integration with website forms, email inboxes, or CRM systems.
- Deterministic extraction and validation for critical numerical fields.
- Evidence tracking for every extracted value.
- Automated duplicate detection using configurable matching rules.
- A shared database configuration and migration system.
- Human review screens for uncertain extractions.
- Improved audit trails for approval and email decisions.
- Automated tests for quantity parsing, product splitting, date extraction, and database insertion.
- Background processing for large volumes of enquiries.
- Role-based access control for dashboard users.
- Deployment using Docker or a cloud hosting platform.
- LinkedIn token management and publishing-status tracking.

## \

## 👨‍💻 Project Summary

The Moti Packaging AI-Powered Enquiry Management System combines LLM-based information extraction, structured validation, SQLite storage, automated customer communication, interactive analytics, and LinkedIn marketing tools in a Python-based application.

Its primary objective is to reduce manual enquiry processing, organize product-specific customer requirements, identify missing information, and support sales teams with a more consistent workflow while retaining human oversight for important decisions.