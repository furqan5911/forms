import streamlit as st
import PyPDF2
import datetime


def extract_pdf_data(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract and map values from extracted text
# def extract_values(text):
#     # Initialize an empty dictionary to store the extracted data
#     data = {}

#     # Split the text by lines to process line by line
#     lines = text.splitlines()

#     # Define keywords to search for in the text
#     keywords = {
#         "name": "Name:",
#         "address": "Business Address:",
#         "ein": "Employer Identification Number (EIN):",
#         "date_incorporated": "Incorporation Date:",
#         "gross_receipts": "Gross Receipts or Sales:",
#         "returns_allowances": "Returns and Allowances:",
#         "cost_of_goods_sold": "Cost of Goods Sold:",
#         "dividends": "Dividends:",
#         "interest": "Interest:",
#         "rents": "Gross Rents:",
#         "royalties": "Gross Royalties:",
#         "capital_gain": "Net Capital Gain:",
#         "net_gain": "Net Gain or (Loss):",
#         "salaries_wages": "Salaries and wages:",
#         "repairs_maintenance": "Repairs and maintenance:",
#         "bad_debts": "Bad debts:",
#         "rents_deductions": "Rents:",
#         "taxes_licenses": "Taxes and licenses:",
#         "interest_deductions": "Interest:",
#         "depreciation": "Depreciation:",
#         "advertising": "Advertising:",
#         "other_deductions": "Other Deductions:"
#     }

#     # Iterate over each line and check if it contains any of the keywords
#     for line in lines:
#         for key, keyword in keywords.items():
#             if keyword in line:
#                 # Extract the value after the keyword
#                 value = line.split(":")[1].strip().replace(",", "").replace("$", "")
#                 if key in ["gross_receipts", "returns_allowances", "cost_of_goods_sold", "dividends", "interest", "rents", "royalties", "capital_gain", "net_gain", "salaries_wages", "repairs_maintenance", "bad_debts", "rents_deductions", "taxes_licenses", "interest_deductions", "depreciation", "advertising", "other_deductions"]:
#                     # Convert numeric values to float
#                     value = float(value)
#                 data[key] = value

#     # Return the extracted data
#     return data
def extract_values(text, form_title):
    # Initialize an empty dictionary to store the extracted data
    data = {}

    # Split the text by sections to process the relevant form
    sections = text.split("Form ")

    # Determine the last part of the title to identify the form
    form_identifier = form_title.split(" ")[2]  # Extract "C-Corp" from "Form 1120 C-Corp"

    # Find the section that corresponds to the form identifier
    form_section = ""
    for section in sections:
        if form_identifier in section:
            form_section = section
            break

    if not form_section:
        raise ValueError(f"Form {form_title} not found in the provided PDF text.")

    # Split the form section into lines to process line by line
    lines = form_section.splitlines()

    # Define keywords to search for in the text
    keywords = {
        "name": "Name:",
        "address": "Business Address:",
        "ein": "Employer Identification Number (EIN):",
        "date_incorporated": "Incorporation Date:",
        "gross_receipts": "Gross Receipts or Sales:",
        "returns_allowances": "Returns and Allowances:",
        "cost_of_goods_sold": "Cost of Goods Sold:",
        "dividends": "Dividends:",
        "interest": "Interest:",
        "rents": "Gross Rents:",
        "royalties": "Gross Royalties:",
        "capital_gain": "Net Capital Gain:",
        "net_gain": "Net Gain or (Loss):",
        "salaries_wages": "Salaries and wages:",
        "repairs_maintenance": "Repairs and maintenance:",
        "bad_debts": "Bad debts:",
        "rents_deductions": "Rents:",
        "taxes_licenses": "Taxes and licenses:",
        "interest_deductions": "Interest:",
        "depreciation": "Depreciation:",
        "advertising": "Advertising:",
        "other_deductions": "Other Deductions:"
    }

    # Iterate over each line and check if it contains any of the keywords
    for line in lines:
        for key, keyword in keywords.items():
            if keyword in line:
                # Extract the value after the keyword
                value = line.split(":")[1].strip().replace(",", "").replace("$", "")
                if key in ["gross_receipts", "returns_allowances", "cost_of_goods_sold", "dividends", "interest", "rents", "royalties", "capital_gain", "net_gain", "salaries_wages", "repairs_maintenance", "bad_debts", "rents_deductions", "taxes_licenses", "interest_deductions", "depreciation", "advertising", "other_deductions"]:
                    # Convert numeric values to float
                    value = float(value)
                data[key] = value

    # Return the extracted data
    return data
# Streamlit app
form_title = "Form 1120 C-Corp"
st.title(form_title)

# File uploader
uploaded_file = st.file_uploader("Upload the PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract and process the PDF data
    pdf_text = extract_pdf_data(uploaded_file)
    extracted_data = extract_values(pdf_text,form_title)
    
    # Populate the form with extracted data
    with st.form("f1120_c_corp"):
        st.subheader("Basic Information")
        name = st.text_input("Name", extracted_data.get("name", ""))
        address = st.text_input("Number, Street, and Room or Suite No.", extracted_data.get("address", ""))
        city_state_zip = st.text_input("City or Town, State or Province, Country, and ZIP or Foreign Postal Code", extracted_data.get("city_state_zip", ""))
        ein = st.text_input("Employer Identification Number (EIN)", extracted_data.get("ein", ""))
        date_str = extracted_data.get("date_incorporated", "")
        if date_str:
                date_incorporated = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            date_incorporated = None
        date_incorporated = st.date_input("Date Incorporated", value=date_incorporated)
        total_assets = st.text_input("Total Assets", value=extracted_data.get("total_assets", 0.0))
        
        st.subheader("Section A: Check if applicable")
        consolidated_return = st.checkbox("Consolidated return (attach Form 851)", value=False)
        life_nonlife_consolidated_return = st.checkbox("Life/nonlife consolidated return", value=False)
        personal_holding_company = st.checkbox("Personal holding company (attach Schedule PH)", value=False)
        personal_service_corporation = st.checkbox("Personal service corporation", value=False)
        schedule_m3_attached = st.checkbox("Schedule M-3 attached", value=False)
        initial_return = st.checkbox("Initial return", value=False)
        final_return = st.checkbox("Final return", value=False)
        name_change = st.checkbox("Name change", value=False)
        address_change = st.checkbox("Address change", value=False)
        
        st.subheader("Income")
        gross_receipts = st.number_input("1a. Gross receipts or sales", min_value=0.0, value=extracted_data.get("gross_receipts", 0.0))
        returns_allowances = st.number_input("1b. Returns and allowances", min_value=0.0, value=extracted_data.get("returns_allowances", 0.0))
        balance = st.number_input("1c. Balance (1a - 1b)", min_value=0.0, value=extracted_data.get("gross_receipts", 0.0) - extracted_data.get("returns_allowances", 0.0))
        cost_of_goods_sold = st.number_input("2. Cost of goods sold (attach Form 1125-A)", min_value=0.0, value=extracted_data.get("cost_of_goods_sold", 0.0))
        gross_profit = st.number_input("3. Gross profit (1c - 2)", min_value=0.0, value=balance - cost_of_goods_sold)
        dividends = st.number_input("4. Dividends and inclusions (Schedule C, line 23)", min_value=0.0, value=extracted_data.get("dividends", 0.0))
        interest = st.number_input("5. Interest", min_value=0.0, value=extracted_data.get("interest", 0.0))
        rents = st.number_input("6. Gross rents", min_value=0.0, value=extracted_data.get("rents", 0.0))
        royalties = st.number_input("7. Gross royalties", min_value=0.0, value=extracted_data.get("royalties", 0.0))
        capital_gain = st.number_input("8. Capital gain net income (attach Schedule D (Form 1120))", min_value=0.0, value=extracted_data.get("capital_gain", 0.0))
        net_gain = st.number_input("9. Net gain or (loss) from Form 4797, Part II, line 17 (attach Form 4797)", min_value=0.0, value=extracted_data.get("net_gain", 0.0))
        other_income = st.number_input("10. Other income (attach statement)", min_value=0.0, value=extracted_data.get("other_income", 0.0))
        total_income = st.number_input("11. Total income (Add lines 3 through 10)", min_value=0.0, value=gross_profit + dividends + interest + rents + royalties + capital_gain + net_gain + other_income)

        st.subheader("Deductions")
        compensation_officers = st.number_input("12. Compensation of officers (attach Form 1125-E)", min_value=0.0, value=0.0)
        salaries_wages = st.number_input("13. Salaries and wages (less employment credits)", min_value=0.0, value=0.0)
        repairs_maintenance = st.number_input("14. Repairs and maintenance", min_value=0.0, value=0.0)
        bad_debts = st.number_input("15. Bad debts", min_value=0.0, value=0.0)
        rents_deductions = st.number_input("16. Rents", min_value=0.0, value=0.0)
        taxes_licenses = st.number_input("17. Taxes and licenses", min_value=0.0, value=0.0)
        interest_deductions = st.number_input("18. Interest (see instructions)", min_value=0.0, value=0.0)
        charitable_contributions = st.number_input("19. Charitable contributions", min_value=0.0, value=0.0)
        depreciation = st.number_input("20. Depreciation (attach Form 4562)", min_value=0.0, value=0.0)
        depletion = st.number_input("21. Depletion", min_value=0.0, value=0.0)
        advertising = st.number_input("22. Advertising", min_value=0.0, value=0.0)
        pension_plans = st.number_input("23. Pension, profit-sharing, etc. plans", min_value=0.0, value=0.0)
        employee_benefit_programs = st.number_input("24. Employee benefit programs", min_value=0.0, value=0.0)
        energy_efficient_deductions = st.number_input("25. Energy efficient commercial buildings deduction (attach Form 7205)", min_value=0.0, value=0.0)
        other_deductions = st.number_input("26. Other deductions (attach statement)", min_value=0.0, value=0.0)
        total_deductions = st.number_input("27. Total deductions (Add lines 12 through 26)", min_value=0.0, value=0.0)

        st.subheader("Tax, Refundable Credits, and Payments")
        taxable_income_before_deductions = st.number_input("28. Taxable income before net operating loss deduction and special deductions", min_value=0.0, value=total_income - total_deductions)
        nol_deduction = st.number_input("29a. Net operating loss deduction", min_value=0.0, value=0.0)
        special_deductions = st.number_input("29b. Special deductions (Schedule C, line 24)", min_value=0.0, value=0.0)
        line_29c = st.number_input("29c. Add lines 29a and 29b", min_value=0.0, value=nol_deduction + special_deductions)
        taxable_income = st.number_input("30. Taxable income (Subtract line 29c from line 28)", min_value=0.0, value=taxable_income_before_deductions - line_29c)
        total_tax = st.number_input("31. Total tax (Schedule J, Part I, line 11)", min_value=0.0, value=0.0)
        reserved_future_use = st.number_input("32. Reserved for future use", min_value=0.0, value=0.0)
        total_payments_credits = st.number_input("33. Total payments and credits (Schedule J, Part II, line 23)", min_value=0.0, value=0.0)
        estimated_tax_penalty = st.number_input("34. Estimated tax penalty (Check if Form 2220 is attached)", min_value=0.0, value=0.0)
        amount_owed = st.number_input("35. Amount owed (if line 33 is smaller than the total of lines 31 and 34)", min_value=0.0, value=0.0)
        overpayment = st.number_input("36. Overpayment (if line 33 is larger than the total of lines 31 and 34)", min_value=0.0, value=0.0)
        credit_to_2024_estimated_tax = st.number_input("37. Enter amount from line 36 you want: Credited to 2024 estimated tax", min_value=0.0, value=0.0)
        refunded_amount = st.number_input("37. Enter amount from line 36 you want: Refunded", min_value=0.0, value=0.0)

        st.subheader("Schedule C: Dividends and Special Deductions")

        def input_row(label, a_key, b_key, c_key):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.number_input(label, min_value=0.0, key=a_key)
            with col2:
                st.number_input("(b) %", min_value=0.0, key=b_key)
            with col3:
                st.number_input("(c) Special Deductions", min_value=0.0, key=c_key)

        input_row("1. Dividends from less-than-20%-owned domestic corporations", "dividends_1a", "dividends_1b", "dividends_1c")
        input_row("2. Dividends from 20%-or-more-owned domestic corporations", "dividends_2a", "dividends_2b", "dividends_2c")
        input_row("3. Dividends on certain debt-financed stock of domestic and foreign corporations", "dividends_3a", "dividends_3b", "dividends_3c")
        input_row("4. Dividends on certain preferred stock of less-than-20%-owned public utilities", "dividends_4a", "dividends_4b", "dividends_4c")
        input_row("5. Dividends on certain preferred stock of 20%-or-more-owned public utilities", "dividends_5a", "dividends_5b", "dividends_5c")
        input_row("6. Dividends from less-than-20%-owned foreign corporations and certain FSCs", "dividends_6a", "dividends_6b", "dividends_6c")
        input_row("7. Dividends from 20%-or-more-owned foreign corporations and certain FSCs", "dividends_7a", "dividends_7b", "dividends_7c")
        input_row("8. Dividends from wholly owned foreign subsidiaries", "dividends_8a", "dividends_8b", "dividends_8c")
        input_row("9. Total (Add lines 1 through 8)", "dividends_total_9a", "dividends_total_9b", "dividends_total_9c")
        input_row("10. Dividends from domestic corporations received by a small business investment company", "dividends_10a", "dividends_10b", "dividends_10c")
        input_row("11. Dividends from affiliated group members", "dividends_11a", "dividends_11b", "dividends_11c")
        input_row("12. Dividends from certain FSCs", "dividends_12a", "dividends_12b", "dividends_12c")
        input_row("13. Foreign-source portion of dividends received from a specified 10%-owned foreign corporation", "dividends_13a", "dividends_13b", "dividends_13c")
        input_row("14. Dividends from foreign corporations not included on lines 3, 6, 7, 8, 11, 12, or 13", "dividends_14a", "dividends_14b", "dividends_14c")
        input_row("15. Reserved for future use", "dividends_15a", "dividends_15b", "dividends_15c")
        input_row("16a. Subpart F inclusions derived from the sale by a CFC of the stock of a lower-tier foreign corporation", "dividends_16a_a", "dividends_16a_b", "dividends_16a_c")
        input_row("16b. Subpart F inclusions derived from hybrid dividends of tiered corporations", "dividends_16b_a", "dividends_16b_b", "dividends_16b_c")
        input_row("16c. Other inclusions from CFCs under subpart F not included on line 16a, 16b, or 17", "dividends_16c_a", "dividends_16c_b", "dividends_16c_c")
        input_row("17. Global Intangible Low-Taxed Income (GILTI)", "dividends_17a", "dividends_17b", "dividends_17c")
        input_row("18. Gross-up for foreign taxes deemed paid", "dividends_18a", "dividends_18b", "dividends_18c")
        input_row("19. IC-DISC and former DISC dividends not included on line 1, 2, or 3", "dividends_19a", "dividends_19b", "dividends_19c")
        input_row("20. Other dividends", "dividends_20a", "dividends_20b", "dividends_20c")
        input_row("21. Deduction for dividends paid on certain preferred stock of public utilities", "dividends_21a", "dividends_21b", "dividends_21c")
        input_row("22. Section 250 deduction", "dividends_22a", "dividends_22b", "dividends_22c")
        input_row("23. Total dividends and inclusions. Add column (a), lines 9 through 20. Enter here and on page 1, line 4", "dividends_23a", "dividends_23b", "dividends_23c")
        input_row("24. Total special deductions. Add column (c), lines 9 through 22. Enter here and on page 1, line 29b", "special_deductions_24a", "special_deductions_24b", "special_deductions_24c")

        st.subheader("Schedule J: Tax Computation and Payment")

        st.write("### Part I—Tax Computation")
        income_tax = st.number_input("1. Income tax. See instructions", min_value=0.0, key="tax_comp_1")
        base_erosion_tax = st.number_input("2. Base erosion minimum tax amount (attach Form 8991)", min_value=0.0, key="tax_comp_2")
        corporate_minimum_tax = st.number_input("3. Corporate alternative minimum tax from Form 4626, Part II, line 13 (attach Form 4626)", min_value=0.0, key="tax_comp_3")
        add_lines_1_2_3 = st.number_input("4. Add lines 1, 2, and 3", min_value=0.0, key="tax_comp_4")
        foreign_tax_credit = st.number_input("5a. Foreign tax credit (attach Form 1118)", min_value=0.0, key="tax_comp_5a")
        credit_form_8834 = st.number_input("5b. Credit from Form 8834 (see instructions)", min_value=0.0, key="tax_comp_5b")
        general_business_credit = st.number_input("5c. General business credit (see instructions—attach Form 3800)", min_value=0.0, key="tax_comp_5c")
        credit_prior_year_min_tax = st.number_input("5d. Credit for prior year minimum tax (attach Form 8827)", min_value=0.0, key="tax_comp_5d")
        bond_credits = st.number_input("5e. Bond credits from Form 8912", min_value=0.0, key="tax_comp_5e")
        total_credits = st.number_input("6. Total credits. Add lines 5a through 5e", min_value=0.0, key="tax_comp_6")
        subtract_line_6 = st.number_input("7. Subtract line 6 from line 4", min_value=0.0, key="tax_comp_7")
        personal_holding_tax = st.number_input("8. Personal holding company tax (attach Schedule PH (Form 1120))", min_value=0.0, key="tax_comp_8")
        recapture_investment_credit = st.number_input("9a. Recapture of investment credit (attach Form 4255)", min_value=0.0, key="tax_comp_9a")
        recapture_low_income_housing_credit = st.number_input("9b. Recapture of low-income housing credit (attach Form 8611)", min_value=0.0, key="tax_comp_9b")
        interest_due_long_term_contracts = st.number_input("9c. Interest due under the look-back method—completed long-term contracts (attach Form 8697)", min_value=0.0, key="tax_comp_9c")
        interest_due_income_forecast_method = st.number_input("9d. Interest due under the look-back method—income forecast method (attach Form 8866)", min_value=0.0, key="tax_comp_9d")
        alternative_tax_qualifying_shipping = st.number_input("9e. Alternative tax on qualifying shipping activities (attach Form 8902)", min_value=0.0, key="tax_comp_9e")
        interest_tax_due_section_453A = st.number_input("9f. Interest/tax due under section 453A(c)", min_value=0.0, key="tax_comp_9f")
        interest_tax_due_section_453l = st.number_input("9g. Interest/tax due under section 453(l)", min_value=0.0, key="tax_comp_9g")
        other_tax_due = st.number_input("9z. Other (see instructions—attach statement)", min_value=0.0, key="tax_comp_9z")
        total_add_lines_9 = st.number_input("10. Total. Add lines 9a through 9z", min_value=0.0, key="tax_comp_10")
        total_tax_computation = st.number_input("11. Total tax. Add lines 7, 8, and 10", min_value=0.0, key="tax_comp_11")

        st.write("### Part II—Payments and Refundable Credits")
        reserved_for_future_use_12 = st.number_input("12. Reserved for future use", min_value=0.0, key="pay_refund_12")
        overpayment_from_prior_year = st.number_input("13. Preceding year’s overpayment credited to the current year", min_value=0.0, key="pay_refund_13")
        estimated_tax_payments = st.number_input("14. Current year’s estimated tax payments", min_value=0.0, key="pay_refund_14")
        current_year_refund_applied = st.number_input("15. Current year’s refund applied for on Form 4466", min_value=0.0, key="pay_refund_15")
        combine_lines_13_14_15 = st.number_input("16. Combine lines 13, 14, and 15", min_value=0.0, key="pay_refund_16")
        tax_deposited_with_form_7004 = st.number_input("17. Tax deposited with Form 7004", min_value=0.0, key="pay_refund_17")
        withholding_tax = st.number_input("18. Withholding (see instructions)", min_value=0.0, key="pay_refund_18")
        total_payments_credits_19 = st.number_input("19. Total payments. Add lines 16, 17, and 18", min_value=0.0, key="pay_refund_19")
        refundable_credits_form_2439 = st.number_input("20a. Refundable credits from Form 2439", min_value=0.0, key="pay_refund_20a")
        refundable_credits_form_4136 = st.number_input("20b. Refundable credits from Form 4136", min_value=0.0, key="pay_refund_20b")
        reserved_for_future_use_20c = st.number_input("20c. Reserved for future use", min_value=0.0, key="pay_refund_20c")
        other_credits = st.number_input("20z. Other (attach statement—see instructions)", min_value=0.0, key="pay_refund_20z")
        total_credits_21 = st.number_input("21. Total credits. Add lines 20a through 20z", min_value=0.0, key="pay_refund_21")
        elective_payment_election = st.number_input("22. Elective payment election amount from Form 3800", min_value=0.0, key="pay_refund_22")
        total_payments_credits_23 = st.number_input("23. Total payments and credits. Add lines 19, 21, and 22", min_value=0.0, key="pay_refund_23")

        st.subheader("Schedule K: Other Information")

        accounting_method = st.selectbox("1. Check accounting method:", ["Cash", "Accrual", "Other (specify)"], key="accounting_method")

        business_activity_code = st.text_input("2a. Business activity code no.", key="business_activity_code")
        business_activity = st.text_input("2b. Business activity", key="business_activity")
        product_or_service = st.text_input("2c. Product or service", key="product_or_service")

        subsidiary_or_parent = st.radio("3. Is the corporation a subsidiary in an affiliated group or a parent–subsidiary controlled group?", ["Yes", "No"], key="subsidiary_or_parent")
        parent_corporation = st.text_input("If Yes, enter name and EIN of the parent corporation", key="parent_corporation")

        st.subheader("4. At the end of the tax year:")
        foreign_domestic_ownership = st.radio("a. Did any foreign or domestic corporation, partnership, trust, or tax-exempt organization own directly 20% or more, or own, directly or indirectly, 50% or more of the total voting power of all classes of the corporation’s stock entitled to vote?", ["Yes", "No"], key="foreign_domestic_ownership")
        if foreign_domestic_ownership == "Yes":
            corp_name = st.text_input("Name of Corporation", key="corp_name")
            corp_ein = st.text_input("Employer Identification Number (if any)", key="corp_ein")
            corp_country = st.text_input("Country of Incorporation", key="corp_country")
            corp_voting_percentage = st.text_input("Percentage Owned in Voting Stock", key="corp_voting_percentage")

        individual_estate_ownership = st.radio("b. Did any individual or estate own directly 20% or more, or own, directly or indirectly, 50% or more of the total voting power of all classes of the corporation’s stock entitled to vote?", ["Yes", "No"], key="individual_estate_ownership")

        st.subheader("5. At the end of the tax year:")
        direct_ownership = st.radio("a. Own directly 20% or more, or own, directly or indirectly, 50% or more of the total voting power of all classes of stock entitled to vote of any foreign or domestic corporation not included on Form 851, Affiliations Schedule?", ["Yes", "No"], key="direct_ownership")
        if direct_ownership == "Yes":
            direct_corp_name = st.text_input("Name of Corporation", key="direct_corp_name")
            direct_corp_ein = st.text_input("Employer Identification Number (if any)", key="direct_corp_ein")
            direct_corp_country = st.text_input("Country of Incorporation", key="direct_corp_country")
            direct_corp_voting_percentage = st.text_input("Percentage Owned in Voting Stock", key="direct_corp_voting_percentage")

        partnership_interest = st.radio("b. Own directly an interest of 20% or more, or own, directly or indirectly, an interest of 50% or more in any foreign or domestic partnership or in the beneficial interest of a trust?", ["Yes", "No"], key="partnership_interest")
        if partnership_interest == "Yes":
            entity_name = st.text_input("Name of Entity", key="entity_name")
            entity_ein = st.text_input("Employer Identification Number (if any)", key="entity_ein")
            entity_country = st.text_input("Country of Organization", key="entity_country")
            entity_percentage = st.text_input("Maximum Percentage Owned in Profit, Loss, or Capital", key="entity_percentage")

        dividends_paid = st.radio("6. During this tax year, did the corporation pay dividends in excess of the corporation’s current and accumulated earnings and profits?", ["Yes", "No"], key="dividends_paid")
        if dividends_paid == "Yes":
            form_5452 = st.text_input("If Yes, file Form 5452 (attach statement)", key="form_5452")

        foreign_person_ownership = st.radio("7. At any time during this tax year, did one foreign person own at least 25% of the total voting power of all classes of the corporation’s stock?", ["Yes", "No"], key="foreign_person_ownership")
        if foreign_person_ownership == "Yes":
            foreign_person_percentage = st.number_input("Percentage Owned", min_value=0.0, max_value=100.0, key="foreign_person_percentage")
            owner_country = st.text_input("Owner’s Country", key="owner_country")
            forms_5472 = st.number_input("Number of Forms 5472 attached", min_value=0, key="forms_5472")

        debt_instruments = st.checkbox("8. Did the corporation issue publicly offered debt instruments with original issue discount?", key="debt_instruments")
        if debt_instruments:
            form_8281 = st.text_input("If Yes, file Form 8281", key="form_8281")

        tax_exempt_interest = st.number_input("9. Enter the amount of tax-exempt interest received or accrued during this tax year", min_value=0.0, key="tax_exempt_interest")

        number_of_shareholders = st.number_input("10. Enter the number of shareholders at the end of the tax year (if 100 or fewer)", min_value=0, key="number_of_shareholders")

        nol_election = st.checkbox("11. If the corporation has an NOL for the tax year and is electing to forego the carryback period, check here", key="nol_election")

        nol_carryover = st.number_input("12. Enter the available NOL carryover from prior tax years", min_value=0.0, key="nol_carryover")

        receipts_assets = st.radio("13. Are the corporation’s total receipts and total assets at the end of the tax year less than $250,000?", ["Yes", "No"], key="receipts_assets")
        if receipts_assets == "Yes":
            cash_distributions = st.number_input("Enter the total amount of cash distributions made during this tax year", min_value=0.0, key="cash_distributions")
            property_distributions = st.number_input("Enter the book value of property distributions made during this tax year", min_value=0.0, key="property_distributions")

        schedule_utp = st.radio("14. Is the corporation required to file Schedule UTP (Form 1120), Uncertain Tax Position Statement?", ["Yes", "No"], key="schedule_utp")

        form_1099_required = st.radio("15a. Did the corporation make any payments that would require it to file Form(s) 1099?", ["Yes", "No"], key="form_1099_required")
        if form_1099_required == "Yes":
            form_1099_filed = st.radio("15b. Did or will the corporation file required Form(s) 1099?", ["Yes", "No"], key="form_1099_filed")

        change_in_ownership = st.radio("16. During this tax year, did the corporation have an 80%-or-more change in ownership, including a change due to redemption of its own stock?", ["Yes", "No"], key="change_in_ownership")

        asset_disposal = st.radio("17. During or subsequent to this tax year, but before the filing of this return, did the corporation dispose of more than 65% (by value) of its assets in a taxable, non-taxable, or tax-deferred transaction?", ["Yes", "No"], key="asset_disposal")

        section_351_transfer = st.radio("18. Did this corporation receive assets in a section 351 transfer in which any of the transferred assets had a fair market basis or fair market value of more than $1 million?", ["Yes", "No"], key="section_351_transfer")

        form_1042_required = st.radio("19. During this corporation’s tax year, did the corporation make any payments that would require it to file Forms 1042 and 1042-S under chapter 3 or chapter 4 of the Code?", ["Yes", "No"], key="form_1042_required")

        cooperative_basis = st.radio("20. Is the corporation operating on a cooperative basis?", ["Yes", "No"], key="cooperative_basis")

        section_267A_interest = st.radio("21. During this tax year, did the corporation pay or accrue any interest or royalty for which the deduction is not allowed under section 267A?", ["Yes", "No"], key="section_267A_interest")

        gross_receipts_500m = st.radio("22. Does this corporation have gross receipts of at least $500 million in any of the 3 preceding tax years?", ["Yes", "No"], key="gross_receipts_500m")

        section_163j_election = st.radio("23. Did the corporation have an election under section 163(j) for any real property trade or business or any farming business in effect during this tax year?", ["Yes", "No"], key="section_163j_election")

        form_8990 = st.radio("24. Does the corporation satisfy one or more of the following? If 'Yes,' complete and attach Form 8990.", ["Yes", "No"], key="form_8990")
        if form_8990 == "Yes":
            pass_through_entity = st.checkbox("a. The corporation owns a pass-through entity with current, or prior year carryover, excess business interest expense.", key="pass_through_entity")
            gross_receipts_29m = st.checkbox("b. The corporation’s aggregate average annual gross receipts for the 3 tax years preceding the current tax year are more than $29 million and the corporation has business interest expense.", key="gross_receipts_29m")
            tax_shelter = st.checkbox("c. The corporation is a tax shelter and the corporation has business interest expense.", key="tax_shelter")

        form_8996 = st.radio("25. Is the corporation attaching Form 8996 to certify as a Qualified Opportunity Fund?", ["Yes", "No"], key="form_8996")
        if form_8996 == "Yes":
            form_8996_amount = st.number_input("If 'Yes,' enter amount from Form 8996, line 15.", min_value=0.0, key="form_8996_amount")

        foreign_corp_acquisition = st.radio("26. Since December 22, 2017, did a foreign corporation directly or indirectly acquire substantially all of the properties held directly or indirectly by the corporation, and was the ownership percentage for purposes of section 7874 greater than 50%?", ["Yes", "No"], key="foreign_corp_acquisition")
        if foreign_corp_acquisition == "Yes":
            ownership_percentage_vote = st.text_input("If 'Yes,' list the ownership percentage by vote.", key="ownership_percentage_vote")
            ownership_percentage_value = st.text_input("If 'Yes,' list the ownership percentage by value.", key="ownership_percentage_value")

        digital_asset_activity = st.radio("27. At any time during this tax year, did the corporation (a) receive a digital asset (as a reward, award, or payment for property or services); or (b) sell, exchange, or otherwise dispose of a digital asset (or a financial interest in a digital asset)?", ["Yes", "No"], key="digital_asset_activity")

        controlled_group = st.radio("28. Is the corporation a member of a controlled group?", ["Yes", "No"], key="controlled_group")
        if controlled_group == "Yes":
            schedule_o = st.text_input("If 'Yes,' attach Schedule O (Form 1120).", key="schedule_o")

        st.subheader("Corporate Alternative Minimum Tax:")
        applicable_corporation_prior = st.radio("29a. Was the corporation an applicable corporation under section 59(k)(1) in any prior tax year?", ["Yes", "No"], key="applicable_corporation_prior")
        if applicable_corporation_prior == "Yes":
            applicable_corporation_current = st.radio("29b. Is the corporation an applicable corporation under section 59(k)(1) in the current tax year because the corporation was an applicable corporation in the prior tax year?", ["Yes", "No"], key="applicable_corporation_current")
            if applicable_corporation_current == "Yes":
                form_4626 = st.text_input("If 'Yes,' complete and attach Form 4626.", key="form_4626")
        safe_harbor = st.radio("29c. Does the corporation meet the requirements of the safe harbor method as provided under section 59(k)(3)(A) for the current tax year?", ["Yes", "No"], key="safe_harbor")
        if safe_harbor == "No":
            form_4626_safe_harbor = st.text_input("If 'No,' complete and attach Form 4626.", key="form_4626_safe_harbor")

        st.subheader("Form 7208:")
        form_7208_required = st.radio("30a. Is the corporation required to file Form 7208 under the rules for stock repurchased by a covered corporation?", ["Yes", "No"], key="form_7208_required")
        form_7208_foreign = st.radio("30b. Is the corporation required to file Form 7208 under the applicable foreign corporation rules?", ["Yes", "No"], key="form_7208_foreign")
        form_7208_surrogate = st.radio("30c. Is the corporation required to file Form 7208 under the covered surrogate foreign corporation rules?", ["Yes", "No"], key="form_7208_surrogate")

        consolidated_return = st.radio("31. Is this a consolidated return with gross receipts or sales of $1 billion or more and a subchapter K basis adjustment of $10 million or more?", ["Yes", "No"], key="consolidated_return")
        if consolidated_return == "Yes":
            attach_statement = st.text_input("If 'Yes,' attach a statement.", key="attach_statement")
        
        st.subheader("Schedule L: Balance Sheets per Books")

        def balance_sheet_row(label, key_a, key_b, key_c, key_d):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.number_input(f"{label} - Beginning of tax year (a)", min_value=0.0, key=key_a)
            with col2:
                st.number_input(f"End of tax year (b)", min_value=0.0, key=key_b)
            with col3:
                st.number_input(f"Beginning of tax year (c)", min_value=0.0, key=key_c)
            with col4:
                st.number_input(f"End of tax year (d)", min_value=0.0, key=key_d)

        balance_sheet_row("1. Cash", "cash_a", "cash_b", "cash_c", "cash_d")
        balance_sheet_row("2a. Trade notes and accounts receivable", "receivables_a", "receivables_b", "receivables_c", "receivables_d")
        balance_sheet_row("2b. Less allowance for bad debts", "bad_debts_a", "bad_debts_b", "bad_debts_c", "bad_debts_d")
        balance_sheet_row("3. Inventories", "inventories_a", "inventories_b", "inventories_c", "inventories_d")
        balance_sheet_row("4. U.S. government obligations", "us_gov_obligations_a", "us_gov_obligations_b", "us_gov_obligations_c", "us_gov_obligations_d")
        balance_sheet_row("5. Tax-exempt securities", "tax_exempt_securities_a", "tax_exempt_securities_b", "tax_exempt_securities_c", "tax_exempt_securities_d")
        balance_sheet_row("6. Other current assets", "other_current_assets_a", "other_current_assets_b", "other_current_assets_c", "other_current_assets_d")
        balance_sheet_row("7. Loans to shareholders", "loans_to_shareholders_a", "loans_to_shareholders_b", "loans_to_shareholders_c", "loans_to_shareholders_d")
        balance_sheet_row("8. Mortgage and real estate loans", "mortgage_loans_a", "mortgage_loans_b", "mortgage_loans_c", "mortgage_loans_d")
        balance_sheet_row("9. Other investments", "other_investments_a", "other_investments_b", "other_investments_c", "other_investments_d")
        balance_sheet_row("10a. Buildings and other depreciable assets", "buildings_a", "buildings_b", "buildings_c", "buildings_d")
        balance_sheet_row("10b. Less accumulated depreciation", "accumulated_depreciation_a", "accumulated_depreciation_b", "accumulated_depreciation_c", "accumulated_depreciation_d")
        balance_sheet_row("11a. Depletable assets", "depletable_assets_a", "depletable_assets_b", "depletable_assets_c", "depletable_assets_d")
        balance_sheet_row("11b. Less accumulated depletion", "accumulated_depletion_a", "accumulated_depletion_b", "accumulated_depletion_c", "accumulated_depletion_d")
        balance_sheet_row("12. Land (net of any amortization)", "land_a", "land_b", "land_c", "land_d")
        balance_sheet_row("13a. Intangible assets (amortizable only)", "intangible_assets_a", "intangible_assets_b", "intangible_assets_c", "intangible_assets_d")
        balance_sheet_row("13b. Less accumulated amortization", "accumulated_amortization_a", "accumulated_amortization_b", "accumulated_amortization_c", "accumulated_amortization_d")
        balance_sheet_row("14. Other assets", "other_assets_a", "other_assets_b", "other_assets_c", "other_assets_d")
        balance_sheet_row("15. Total assets", "total_assets_a", "total_assets_b", "total_assets_c", "total_assets_d")

        st.subheader("Liabilities and Shareholders’ Equity")

        balance_sheet_row("16. Accounts payable", "accounts_payable_a", "accounts_payable_b", "accounts_payable_c", "accounts_payable_d")
        balance_sheet_row("17. Mortgages, notes, bonds payable in less than 1 year", "mortgages_notes_1yr_a", "mortgages_notes_1yr_b", "mortgages_notes_1yr_c", "mortgages_notes_1yr_d")
        balance_sheet_row("18. Other current liabilities", "other_current_liabilities_a", "other_current_liabilities_b", "other_current_liabilities_c", "other_current_liabilities_d")
        balance_sheet_row("19. Loans from shareholders", "loans_from_shareholders_a", "loans_from_shareholders_b", "loans_from_shareholders_c", "loans_from_shareholders_d")
        balance_sheet_row("20. Mortgages, notes, bonds payable in 1 year or more", "mortgages_notes_1plus_a", "mortgages_notes_1plus_b", "mortgages_notes_1plus_c", "mortgages_notes_1plus_d")
        balance_sheet_row("21. Other liabilities", "other_liabilities_a", "other_liabilities_b", "other_liabilities_c", "other_liabilities_d")
        balance_sheet_row("22a. Preferred stock", "preferred_stock_a", "preferred_stock_b", "preferred_stock_c", "preferred_stock_d")
        balance_sheet_row("22b. Common stock", "common_stock_a", "common_stock_b", "common_stock_c", "common_stock_d")
        balance_sheet_row("23. Additional paid-in capital", "paid_in_capital_a", "paid_in_capital_b", "paid_in_capital_c", "paid_in_capital_d")
        balance_sheet_row("24. Retained earnings—Appropriated", "retained_earnings_appropriated_a", "retained_earnings_appropriated_b", "retained_earnings_appropriated_c", "retained_earnings_appropriated_d")
        balance_sheet_row("25. Retained earnings—Unappropriated", "retained_earnings_unappropriated_a", "retained_earnings_unappropriated_b", "retained_earnings_unappropriated_c", "retained_earnings_unappropriated_d")
        balance_sheet_row("26. Adjustments to shareholders’ equity", "adjustments_equity_a", "adjustments_equity_b", "adjustments_equity_c", "adjustments_equity_d")
        balance_sheet_row("27. Less cost of treasury stock", "cost_treasury_stock_a", "cost_treasury_stock_b", "cost_treasury_stock_c", "cost_treasury_stock_d")
        balance_sheet_row("28. Total liabilities and shareholders’ equity", "total_liabilities_equity_a", "total_liabilities_equity_b", "total_liabilities_equity_c", "total_liabilities_equity_d")

        st.subheader("Schedule M-1: Reconciliation of Income (Loss) per Books With Income per Return")
        m1_net_income_books = st.number_input("1. Net income (loss) per books", min_value=0.0, key="m1_net_income_books")
        m1_federal_income_tax = st.number_input("2. Federal income tax per books", min_value=0.0, key="m1_federal_income_tax")
        m1_excess_capital_losses = st.number_input("3. Excess of capital losses over capital gains", min_value=0.0, key="m1_excess_capital_losses")
        m1_income_subject_tax = st.text_input("4. Income subject to tax not recorded on books this year (itemize)", key="m1_income_subject_tax")
        m1_depreciation = st.number_input("5a. Depreciation", min_value=0.0, key="m1_depreciation")
        m1_charitable_contributions = st.number_input("5b. Charitable contributions", min_value=0.0, key="m1_charitable_contributions")
        m1_travel_entertainment = st.number_input("5c. Travel and entertainment", min_value=0.0, key="m1_travel_entertainment")
        m1_total_income = st.number_input("6. Add lines 1 through 5", min_value=0.0, key="m1_total_income")
        m1_income_not_included = st.text_input("7. Income recorded on books this year not included on this return (itemize):", key="m1_income_not_included")
        m1_depreciation_deductions = st.number_input("8a. Depreciation", min_value=0.0, key="m1_depreciation_deductions")
        m1_charitable_contributions_deductions = st.number_input("8b. Charitable contributions", min_value=0.0, key="m1_charitable_contributions_deductions")
        m1_total_deductions = st.number_input("9. Add lines 7 and 8", min_value=0.0, key="m1_total_deductions")
        m1_final_income = st.number_input("10. Income (page 1, line 28)—line 6 less line 9", min_value=0.0, key="m1_final_income")

        st.subheader("Schedule M-2: Analysis of Unappropriated Retained Earnings per Books (Schedule L, Line 25)")
        m2_balance_beginning = st.number_input("1. Balance at beginning of year", min_value=0.0, key="m2_balance_beginning")
        m2_net_income_books = st.number_input("2. Net income (loss) per books", min_value=0.0, key="m2_net_income_books")
        m2_other_increases = st.text_input("3. Other increases (itemize):", key="m2_other_increases")
        m2_total_additions = st.number_input("4. Add lines 1, 2, and 3", min_value=0.0, key="m2_total_additions")
        m2_distributions = st.text_input("5. Distributions:", key="m2_distributions")
        m2_cash_distributions = st.number_input("   a. Cash", min_value=0.0, key="m2_cash_distributions")
        m2_stock_distributions = st.number_input("   b. Stock", min_value=0.0, key="m2_stock_distributions")
        m2_property_distributions = st.number_input("   c. Property", min_value=0.0, key="m2_property_distributions")
        m2_other_decreases = st.text_input("6. Other decreases (itemize):", key="m2_other_decreases")
        m2_total_decreases = st.number_input("7. Add lines 5 and 6", min_value=0.0, key="m2_total_decreases")
        m2_final_balance = st.number_input("8. Balance at end of year (line 4 less line 7)", min_value=0.0, key="m2_final_balance")

        submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Form 1120 C-Corp submitted successfully!")






