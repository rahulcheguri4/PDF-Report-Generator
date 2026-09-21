def create_pdf():
    file_name = "report.pdf"

    # Business data
    products = [
        ["Product", "Category", "Sales", "Quantity"],
        ["Laptop", "Electronics", "55000", "5"],
        ["Mobile", "Electronics", "30000", "10"],
        ["Chair", "Furniture", "15000", "8"],
        ["Table", "Furniture", "25000", "5"],
        ["Headphones", "Electronics", "10000", "20"]
    ]

    # Calculate summary
    total_products = len(products) - 1
    total_sales = 0
    total_quantity = 0

    for row in products[1:]:
        total_sales += int(row[2])
        total_quantity += int(row[3])

    # Create PDF content
    lines = []

    lines.append("BUSINESS SALES REPORT")
    lines.append("")
    lines.append("SUMMARY")
    lines.append("------------------------------")
    lines.append("Total Products : " + str(total_products))
    lines.append("Total Quantity : " + str(total_quantity))
    lines.append("Total Sales    : Rs. " + str(total_sales))
    lines.append("")
    lines.append("SALES DETAILS")
    lines.append("------------------------------")

    # Add table
    for row in products:
        line = " | ".join(row)
        lines.append(line)

    # PDF content
    pdf = []

    pdf.append(b"%PDF-1.4\n")

    # Objects
    objects = []

    objects.append(
        b"<< /Type /Catalog /Pages 2 0 R >>"
    )

    objects.append(
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>"
    )

    objects.append(
        b"<< /Type /Page /Parent 2 0 R "
        b"/MediaBox [0 0 595 842] "
        b"/Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>"
    )

    # Text
    text = "BT\n/F1 11 Tf\n50 800 Td\n"

    for line in lines:
        safe_line = line.replace("\\", "\\\\")
        safe_line = safe_line.replace("(", "\\(")
        safe_line = safe_line.replace(")", "\\)")

        text += "(" + safe_line + ") Tj\n"
        text += "0 -18 Td\n"

    text += "ET"

    text_bytes = text.encode("latin-1")

    objects.append(
        b"<< /Length " +
        str(len(text_bytes)).encode() +
        b" >>\nstream\n" +
        text_bytes +
        b"\nendstream"
    )

    objects.append(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    )

    # Write PDF
    offsets = [0]

    for i, obj in enumerate(objects, start=1):
        offsets.append(sum(len(x) for x in pdf))

        pdf.append(
            str(i).encode() + b" 0 obj\n"
        )

        pdf.append(obj)

        pdf.append(b"\nendobj\n")

    xref_position = sum(len(x) for x in pdf)

    pdf.append(
        b"xref\n0 " +
        str(len(objects) + 1).encode() +
        b"\n"
    )

    pdf.append(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.append(
            f"{offset:010d} 00000 n \n".encode()
        )

    pdf.append(
        b"trailer\n"
        b"<< /Size " +
        str(len(objects) + 1).encode() +
        b" /Root 1 0 R >>\n"
    )

    pdf.append(
        b"startxref\n" +
        str(xref_position).encode() +
        b"\n%%EOF"
    )

    # Save PDF
    with open(file_name, "wb") as file:
        for part in pdf:
            file.write(part)

    print("PDF report generated successfully!")
    print("File name:", file_name)


# Run program
create_pdf()