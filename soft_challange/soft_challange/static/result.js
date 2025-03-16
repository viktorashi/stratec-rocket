function travelFormSubmitHandler() {
    const travelForm = document.forms['travelForm']
    const submitterButton = document.getElementById('travelSubmitButton')

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
