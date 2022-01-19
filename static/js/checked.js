 $(".checkAnswer").on('click', function (ev) {
     let $this = $(this)
     let checked = document.getElementById($this.data('id')).checked

     $.ajax({
         method: "POST",
         url: "/correct/",
         data: {'id': $this.data('id'), 'checked': checked},
         headers: {'X-CSRFToken': csrftoken}
     })
     .done(function(data) {
         document.getElementById($this.data('id')).checked = data['checked']
     });
})