# Data Directory

This directory contains sample data and test files for the Smart Document Extractor.

## Structure

```
data/
├── README.md (this file)
├── samples/          # Sample PDF files for testing
├── templates/        # Field extraction templates
└── examples/         # Example extracted data
```

## Sample Test Data

### Creating Test PDFs

For testing the application, you can use any banking documents:

1. **Loan Application Form**
   - Expected fields: Name, Loan Amount, Employment, IFSC
   
2. **KYC Document**
   - Expected fields: PAN, Aadhar, Address, DOB

3. **Bank Statement**
   - Expected fields: Account Number, Balance, Transactions

## Field Extraction Templates

### Banking Document Fields

```
Standard banking fields:
- Customer Name / Applicant Name / Borrower Name
- Loan Number / Account Number / LAN
- Loan Amount / Loan Value / Principal Amount
- PAN Number / PAN / Tax ID
- IFSC Code / Bank Code
- Account Status / Loan Status
- Sanctioned Amount / Approved Amount
```

### KYC Document Fields

```
KYC fields:
- Full Name
- PAN Number
- Aadhar Number
- Date of Birth
- Address
- Email
- Phone Number
- Occupation
```

## Example Extracted Data

### Loan Document Example

```json
{
    "Customer Name": "John Doe",
    "Loan Number": "LOAN123456789",
    "Loan Amount": "500000",
    "PAN Number": "ABCD1234E",
    "IFSC Code": "HDFC0001234"
}
```

### KYC Document Example

```json
{
    "Full Name": "Jane Smith",
    "PAN Number": "EFGH5678I",
    "Aadhar Number": "1234 5678 9012",
    "Date of Birth": "01/01/1990",
    "Address": "123 Main St, City, State 123456"
}
```

## Testing Workflow

1. Place PDF files in `data/samples/`
2. Use filenames like: `loan_document_01.pdf`, `kyc_form_02.pdf`
3. Run the application
4. Upload sample files and test extraction
5. Verify results match expected output
6. Review logs for any issues

## Data Processing Notes

- Extracted data is stored in `outputs/` directory
- Each extraction creates a timestamped Excel file
- All data remains on your local system
- No data is sent to external servers

## Privacy

- Sample data is for testing only
- Use anonymized or dummy data for development
- Do not store real personal information without proper security
- Ensure compliance with data protection regulations

---

For more information, see [README.md](../README.md)
