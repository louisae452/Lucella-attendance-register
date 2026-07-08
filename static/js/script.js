document.addEventListener("DOMContentLoaded", function() {

// Code written with AI to override browser's default blue colour in dropdown menus 
    const targetDropdownIds = ['id_subject', 'id_parent_name', 'id_teacher_name', 'id_day', 'id_session', 'id_subject_name', 'id_status', 'id_code', 'id_mark', 'id_sex', 'id_group', 'id_music_option'];
    targetDropdownIds.forEach(id => {
        const element = document.getElementById(id);
        // Safety check: Only initialize if the specific element exists on this page
        if (element) {
            new Choices(element, {
                searchEnabled: false, 
                itemSelectText: '',   
            });
            console.log(`Choices.js successfully initialized for #${id}!`);
        } else {
            // Optional: Changed to log instead of error so missing elements don't look like critical bugs
            console.log(`Choices.js skipped #${id} (Element not found on this page).`);
        }
    });
 // End of AI code
    
    // Highlight low attendance percentages.
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

    // Show timetable info
    let buttona =  document.getElementById("buttona");
    let timetablea = document.getElementById("timetablea");
    buttona.addEventListener("click", function() {   
        timetablea.classList.remove('hidden');
    })
    let hidea = document.getElementById("hidea");
    hidea.addEventListener("click", function(){
        timetablea.classList.add('hidden')
    });

    let buttonb =  document.getElementById("buttonb");
    let timetableb = document.getElementById("timetableb");
    buttonb.addEventListener("click", function() {   
        timetableb.classList.remove('hidden');
    })
    let hideb = document.getElementById("hideb");
    hideb.addEventListener("click", function(){
        timetableb.classList.add('hidden')
    })
    





});