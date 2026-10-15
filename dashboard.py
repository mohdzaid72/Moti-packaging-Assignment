import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import requests

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
load_dotenv()


def generate_product_description(product_name, product_prompt):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY missing. Check your .env file."
        )

    llm = ChatGroq(
        model=os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b",
        ),
        temperature=0.7,
        max_tokens=700,
        api_key=api_key,
    )

    messages = [
    (
        "system",
        """
You are an expert LinkedIn copywriter who writes
marketing posts for products across all industries.

YOUR TASK:
Generate a ready-to-publish LinkedIn post using the
product name and details provided by the user.

STRICT RULES:
1. Return ONLY the final LinkedIn post.
2. Never ask questions or request clarification.
3. Never explain your reasoning or mention these instructions.
4. Never include introductions such as "Here is your post".
5. Never refuse or discuss whether the product fits a
   particular industry.
6. Use the exact product name and focus on the product
   described by the user, even if it belongs to an
   industry other than packaging.
7. Do not force a connection to Moti Packaging Industries
   unless the user explicitly requests it.
8. Use only the facts provided. Never invent features,
   specifications, certifications, or benefits.
9. Write in professional, engaging, natural English.
10. Start with a compelling hook, use short paragraphs,
    relevant emojis, a suitable call to action, and
    3-5 relevant hashtags.
11. If the information is limited, write the best possible
    post using the available details without asking questions.
12. Output the post itself and nothing else.
"""
    ),
    (
        "human",
        f"""
Product name:
{product_name}

Product details and writing instructions:
{product_prompt}

Write the final LinkedIn marketing post now.
Return only the post text.
"""
    ),
]


    response = llm.invoke(messages)

    description = response.content

    if not isinstance(description, str) or not description.strip():
        raise ValueError("The AI returned an empty description.")

    return description.strip()

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Packaging Enquiry Dashboard",
    page_icon="📦",
    layout="wide",
)

DB_PATH = Path(__file__).resolve().parent / "LeadData1.db"


# =====================================================
# DATABASE
# =====================================================

@st.cache_data(ttl=5)
def load_data():
    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT rowid AS lead_id, * FROM data",
            conn,
        )


# =====================================================
# HEADER
# =====================================================

st.title("📦 Packaging Enquiry Dashboard")
st.caption("Moti Packaging Industries Pvt. Ltd.")

if st.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

if not DB_PATH.exists():
    st.error(f"Database not found: {DB_PATH}")
    st.info("Place dashboard.py in the same folder as LeadData.db.")
    st.stop()

try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not read the database: {exc}")
    st.stop()

if df.empty:
    st.warning("No enquiries found in the database yet.")
    st.stop()


# =====================================================
# CLEAN DATA
# =====================================================

df.columns = df.columns.str.strip()

if "query_category" not in df.columns:
    st.error("The database does not contain the query_category column.")
    st.stop()

df["query_category"] = (
    df["query_category"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

if "product_category" not in df.columns:
    df["product_category"] = None

df["product_category"] = (
    df["product_category"]
    .fillna("Unknown")
    .replace("", "Unknown")
)

# =====================================================
# KPI COUNTS
# =====================================================

total_enquiries = len(df)

ready_count = (
    df["query_category"] == "ready to quotation"
).sum()

duplicate_count = (
    df["query_category"] == "possible duplicate enquiry"
).sum()

not_serviceable_count = (
    df["query_category"] == "not currently serviceable"
).sum()

missing_lead = df["query_category"].eq("more information required").sum()


# =====================================================
# METRIC CARDS
# =====================================================

st.subheader("Enquiry Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Enquiries",
    f"{total_enquiries:,}",
)

col2.metric(
    "Ready for Quotation",
    f"{ready_count:,}",
)

col3.metric(
    "Duplicate Enquiries",
    f"{duplicate_count:,}",
)

col4.metric(
    "Not Serviceable",
    f"{not_serviceable_count:,}",
)
col1.metric(
    "Information Pending",
    f"{missing_lead}",
)

st.divider()


# =====================================================
# ENQUIRIES BY PRODUCT TYPE
# =====================================================

st.subheader("Enquiries by Product Type")

product_counts = (
    df["product_category"]
    .value_counts()
    .rename_axis("Product Type")
    .reset_index(name="Enquiries")
)

if not product_counts.empty:
    fig = px.bar(
        product_counts,
        x="Product Type",
        y="Enquiries",
        color="Product Type",
        text="Enquiries",
        title="Enquiries by Packaging Category",
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Packaging Category",
        yaxis_title="Number of Enquiries",
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No product category data available.")


# =====================================================
# ENQUIRIES BY STATUS
# =====================================================

st.subheader("Enquiries by Status")

status_labels = {
    "ready to quotation": "Ready for Quotation",
    "more information required": "More Information Required",
    "not currently serviceable": "Not Serviceable",
    "possible duplicate enquiry": "Possible Duplicate",
}

status_df = (
    df["query_category"]
    .replace("", "unknown")
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Enquiries")
)

status_df["Status"] = (
    status_df["Status"]
    .map(status_labels)
    .fillna("Unknown / Other")
)

fig_status = px.pie(
    status_df,
    names="Status",
    values="Enquiries",
    hole=0.45,
    title="Enquiry Status Distribution",
)

st.plotly_chart(fig_status, use_container_width=True)


# =====================================================
# SEARCH AND FILTERS
# =====================================================

st.subheader("Enquiry Records")

search = st.text_input(
    "Search by customer, company, phone, or email"
)

all_categories = sorted(
    df["product_category"].astype(str).unique().tolist()
)

selected_categories = st.multiselect(
    "Filter by product type",
    options=all_categories,
    default=all_categories,
)

all_statuses = sorted(
    df["query_category"].replace("", "unknown").unique().tolist()
)

selected_statuses = st.multiselect(
    "Filter by enquiry status",
    options=all_statuses,
    default=all_statuses,
)

filtered_df = df[
    df["product_category"].astype(str).isin(selected_categories)
    & df["query_category"].replace("", "unknown").isin(selected_statuses)
].copy()

if search.strip():
    search_columns = [
        column for column in [
            "customer_name",
            "company_name",
            "mobile_no",
            "email",
        ]
        if column in filtered_df.columns
    ]

    if search_columns:
        mask = pd.Series(False, index=filtered_df.index)

        for column in search_columns:
            mask |= (
                filtered_df[column]
                .fillna("")
                .astype(str)
                .str.contains(search.strip(), case=False, regex=False)
            )

        filtered_df = filtered_df[mask]

# Use friendly column headings
display_df = filtered_df.rename(
    columns={
        "lead_id": "Lead ID",
        "customer_name": "Customer",
        "company_name": "Company",
        "mobile_no": "Mobile",
        "email": "Email",
        "product_application": "Product Application",
        "product_category": "Product Type",
        "diameter": "Diameter (mm)",
        "height": "Height (mm)",
        "quantity": "Quantity",
        "printing_details": "Printing Details",
        "delivery_location": "Delivery Location",
        "required_date": "Required Date",
        "query_category": "Status",
    }
)

display_columns = [
    column for column in [
        "Lead ID",
        "Customer",
        "Company",
        "Mobile",
        "Email",
        "Product Application",
        "Product Type",
        "Diameter (mm)",
        "Height (mm)",
        "Quantity",
        "Printing Details",
        "Delivery Location",
        "Required Date",
        "Status",
    ]
    if column in display_df.columns
]

st.caption(f"Showing {len(filtered_df):,} of {total_enquiries:,} enquiries")

st.dataframe(
    display_df[display_columns],
    use_container_width=True,
    hide_index=True,
)

# =====================================================
# DOWNLOAD
# =====================================================

csv_data = display_df[display_columns].to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Enquiries as CSV",
    data=csv_data,
    file_name="packaging_enquiries.csv",
    mime="text/csv",
)







import requests

st.divider()
st.header("📣 Post Product on LinkedIn")

product_name = st.text_input(
    "Product Name",
    placeholder="Enter product name"
)

product_prompt = st.text_area(
    "Product Details / AI Prompt",
    placeholder=(
        "Describe the material, features, dimensions, "
        "applications, benefits and target customers..."
    ),
    height=130,
    key="linkedin_product_prompt",)

uploaded_image = st.file_uploader(
    "Upload Product Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Image Preview", width=300)

if "linkedin_description" not in st.session_state:
    st.session_state["linkedin_description"] = ""




generate_clicked = st.button(
    "✨ Generate Description",
    use_container_width=True,
)



if generate_clicked :
    if not product_name.strip():
        st.warning("Please enter the product name.")

    elif not product_prompt.strip():
        st.warning("Please enter the product details.")

    else:
        try:
            with st.spinner("Generating description with Groq AI..."):
                generated_text = generate_product_description(
                    product_name.strip(),
                    product_prompt.strip(),
                )

            st.session_state["linkedin_description"] = generated_text
            st.success("Description generated successfully!")

        except Exception as exc:
            st.error(f"Description generation failed: {exc}")

description = st.text_area(
    "LinkedIn Description (Editable)",
    key="linkedin_description",
    height=250,
    placeholder="Generate a description or write your own...",
)


product_url = st.text_input(
    "Product URL (optional)",
    placeholder="https://motipackaging.com/..."
)

approved = st.checkbox(
    "I have verified the product details and approved this post."
)

if st.button("🚀 Post on LinkedIn", type="primary"):

    if not product_name.strip():
        st.warning("Please enter the product name.")

    elif uploaded_image is None:
        st.warning("Please upload a product image.")

    elif not description.strip():
        st.warning("Please enter the post description.")

    elif not approved:
        st.warning("Please approve the product details first.")

    else:
        try:
            config = st.secrets["linkedin"]
            token = config["access_token"]
            
            version = config["api_version"]

            headers = {
                "Authorization": f"Bearer {token}",
                "LinkedIn-Version": version,
                "X-Restli-Protocol-Version": "2.0.0",
            }

            caption = f"{product_name.strip()}\n\n{description.strip()}"

            if product_url.strip():
                caption += f"\n\nLearn more: {product_url.strip()}"

            owner = f"urn:li:person:{config['member_id']}"

            # 1. Register the image upload
            init = requests.post(
                "https://api.linkedin.com/rest/images?action=initializeUpload",
                headers={
                    **headers,
                    "Content-Type": "application/json",
                },
                json={
                    "initializeUploadRequest": {
                        "owner": owner
                    }
                },
                timeout=30,
            )
            init.raise_for_status()

            upload_info = init.json()["value"]

            # 2. Upload the image
            upload = requests.put(
                upload_info["uploadUrl"],
                data=uploaded_image.getvalue(),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": uploaded_image.type,
                },
                timeout=60,
            )
            upload.raise_for_status()

            # 3. Publish the post
            payload = {
                "author": owner,
                "commentary": caption,
                "visibility": "PUBLIC",
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": [],
                },
                "content": {
                    "media": {
                        "id": upload_info["image"],
                        "altText": f"Product image: {product_name}"[:4000],
                    }
                },
                "lifecycleState": "PUBLISHED",
                "isReshareDisabledByAuthor": False,
            }

            response = requests.post(
                "https://api.linkedin.com/rest/posts",
                headers={
                    **headers,
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )
            response.raise_for_status()

            st.success("Product post published successfully! 🎉")

        except Exception as e:
            st.error(f"Could not publish the post: {e}")