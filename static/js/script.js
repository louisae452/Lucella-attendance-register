document.addEventListener("DOMContentLoaded", function() {
let alerts = document.querySelectorAll('.redalert');
const orange = 90;
const red = 80;
alerts.forEach(number =>{
    let percentage = parseFloat(number.textContent);
    if (percentage < red) {
        number.style.color='var(--red-alert)';
    }else if  (percentage < orange) {
        number.style.color = 'var(--orange-alert)';
    
    }
});





});