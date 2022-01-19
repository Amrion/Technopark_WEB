 $(".vote").on('click', function (ev) {
        let $this = $(this)
        $.ajax({
            method: "POST",
            url: "/vote/",
            data: {'id': $this.data('id'), 'action': $this.data('action'), 'class': $this.data('class')},
            headers: {'X-CSRFToken': csrftoken}
        })
        .done(function(data) {
            if ($this.data('action') === "like") {
                console.log(1)
                document.getElementById($this.data('id') + '-' + $this.data('class')+ '-' + $this.data('action')).innerHTML = data['like']
            } else {
                console.log(2)
                document.getElementById($this.data('id') + '-' + $this.data('class') + '-' + $this.data('action')).innerHTML = data['dislike']
            }
        });
    })