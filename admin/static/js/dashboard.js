console.log("Admin dashboard JS loaded!");

// Example: confirmation before assigning driver
document.addEventListener("DOMContentLoaded", function () {
    const assignForms = document.querySelectorAll("form[action^='/assign_driver/']");
    assignForms.forEach(form => {
        form.addEventListener("submit", function(e){
            const driver = this.querySelector("select[name='driver_id']").selectedOptions[0].text;
            if(!confirm(`Are you sure you want to assign ${driver} to this order?`)) {
                e.preventDefault(); // cancel submit
            }
        });
    });
});
