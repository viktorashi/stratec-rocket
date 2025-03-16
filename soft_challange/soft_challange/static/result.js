function stupidTravelFormSubmitHandler() {
    const travelForm = document.forms['stupidTravelForm']
    const submitterButton = document.getElementById('stupidTravelSubmitButton')

    const formData = new FormData(travelForm, submitterButton);

    if (formData.get('from_planet') === formData.get('to_planet')) {
        const travelError = document.getElementById('travelError')
        travelError.innerText = 'The planets must be different, sillyy'
        travelError.style.display = 'block'
        // it's NOT safe to submit the form
        return false;
    }
    // it's safe to submit the form
    return true;
}


function mediumTravelFormSubmitHandler(){
    const travelForm = document.forms['mediumTravelForm']
    const submitterButton = document.getElementById('mediumTravelSubmitButton')

    const formData = new FormData(travelForm, submitterButton);

    if (formData.get('from_planet') === formData.get('to_planet')) {
        const travelError = document.getElementById('travelError')
        travelError.innerText = 'The planets must be different, sillyy'
        travelError.style.display = 'block'
        // it's NOT safe to submit the form
        return false;
    }
    // it's safe to submit the form
    return true;
}