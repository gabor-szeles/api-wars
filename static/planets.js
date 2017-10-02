$('#nextButton').click(function(){
    var nextPage = document.getElementById('nextButton').dataset.next
    console.log(nextPage)
    $.ajax({
      type: 'POST',
      url: '/',
      data: {"next_page": nextPage}
    })
     .done(function(completeHtmlPage) {
       $("body").empty();
       $("body").append(completeHtmlPage)
    });
})
