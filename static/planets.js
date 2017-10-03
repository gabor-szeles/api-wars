$('#nextButton').click(function(){
    var nextPage = this.dataset.next
    pager(nextPage)

})


$('#prevButton').click(function(){
    var prevPage = this.dataset.prev
    pager(prevPage)

})


function pager(page){
    $.ajax({
      type: 'POST',
      url: '/',
      data: {"next_page": page}
    })
     .done(function(completeHtmlPage) {
       $("body").empty();
       $("body").append(completeHtmlPage)
    });
}


$('#residentsModal').on('show.bs.modal', function(event) {
    var clickedButton = $(event.relatedTarget) // Button that triggered the modal
    console.log(clickedButton)
    var planetName = clickedButton.data('planetname')
    $('.modal-title').text(`Known residents of ${planetName}`)
});
