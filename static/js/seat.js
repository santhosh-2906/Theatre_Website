document.querySelectorAll('label input[type="checkbox"]').forEach(input => {
    input.addEventListener('change', function() {
        if(this.checked){
            this.parentElement.classList.add('bg-success', 'text-white');
            this.parentElement.classList.remove('bg-light');
        } else {
            this.parentElement.classList.remove('bg-success', 'text-white');
            this.parentElement.classList.add('bg-light');
        }
    });
});
