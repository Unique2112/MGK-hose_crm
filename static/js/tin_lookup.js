document.addEventListener('DOMContentLoaded', function() {
    // Django Admin ብዙውን ጊዜ ID የሚሰጠው 'id_' + የፊልዱ ስም በማድረግ ነው
    var tinField = document.querySelector('#id_tin_number');
    var companyField = document.querySelector('#id_company_name');

    if (tinField && companyField) {
        console.log("TIN lookup script is active!"); // ለመሞከር እንዲረዳን

        tinField.addEventListener('blur', function() { // ከሳጥኑ ሲወጡ (Blur) እንዲፈልግ
            var tinValue = this.value.trim();
            if (tinValue) {
                // መረጃውን ከ View ለመጠየቅ
                fetch('/get_customer_by_tin/?tin=' + tinValue)
                    .then(response => response.json())
                    .then(data => {
                        if (data.exists) {
                            companyField.value = data.company_name;
                            // የኩባንያው ስም ሲሞላ አረንጓዴ ከለር ለትንሽ ጊዜ እንዲያሳይ
                            companyField.style.border = '2px solid #28a745';
                            setTimeout(() => {
                                companyField.style.border = '';
                            }, 2000);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    } else {
        console.log("Field IDs not found. Checking for different IDs...");
    }
});