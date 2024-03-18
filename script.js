fetch("data.json")
.then(function(response){
    return response.json();
})
.then(function(data){
    let stockListDiv = document.querySelector("#stock-list");
    let transactionHistoryDiv = document.querySelector("#transaction-history");

    // Display stock list
    let stockListOutput = "<h2>Stock List</h2>";
    stockListOutput += "<table style='border-collapse: collapse;'>";
    stockListOutput += "<thead><tr><th>Stock</th><th>Quantity</th><th>Price</th></tr></thead>";
    stockListOutput += "<tbody>"
    for(let stock in data.stock_list){
        if (data.stock_list.hasOwnProperty(stock)) {
            stockListOutput += `
                    <tr>
                        <td>${stock}</td>
                        <td>${data.stock_list[stock][0]}</td>
                        <td>$${data.stock_list[stock][1].toFixed(2)}</td>
                    </tr>
            `;
        }
    }
    stockListOutput += "</tbody></table>";

    stockListDiv.innerHTML = stockListOutput;

    // Display transaction history
    let transactionHistoryOutput = "<h2>Transaction History</h2>";
    transactionHistoryOutput += "<table style='border-collapse: collapse;'>"; // Removed id attribute
    transactionHistoryOutput += "<thead><tr><th>Date</th><th>Type</th><th>Stock</th><th>Price</th><th>Quantity</th></tr></thead>";
    for(let transaction of data.transaction_history){
        transactionHistoryOutput += "<tbody><tr>";
        for(let i = 0; i < transaction.length; i++){
            if (i === 3) {
                transactionHistoryOutput += `<td>$${transaction[i].toFixed(2)}</td>`; // Apply .toFixed() to the price
            } else {
                transactionHistoryOutput += `<td>${transaction[i]}</td>`;
            }
        }
        transactionHistoryOutput += "</tr></tbody>";
    }
    transactionHistoryOutput += "</table>";

    transactionHistoryDiv.innerHTML = transactionHistoryOutput;

    // Apply CSS to center the table horizontally (optional)
    // let tables = document.querySelectorAll('table');
    // tables.forEach(table => {
    //     table.style.margin = '0 auto'; // Set margin to 'auto' to center horizontally
    // });
});
