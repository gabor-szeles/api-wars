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
      data: {'next_page': page}
    })
     .done(function(completeHtmlPage) {
       $("body").empty();
       $("body").append(completeHtmlPage)
    });
}


$('#residentsModal').on('show.bs.modal', function(event) {
    var clickedButton = $(event.relatedTarget) // Button that triggered the modal
    var planetName = clickedButton.data('planetname')
    var apiList = clickedButton.data('residentapilist')
    apiList = apiList.replace(/'/g, '').slice(1, -1).split(',')
    var residentsArray = []
    for (let api=0; api<apiList.length;api++){
        apiCall(apiList[api])
    }
    $('.modal-title').text(`Known residents of ${planetName}`)
});


$("#residentsModal").on("hidden.bs.modal", function () {
    $(".actual-data").empty()
});


function apiCall(apiLink){
    $.ajax({
        dataType: "json",
        url: apiLink,
        success: function(response) {
            $(".resident-data").append(`<tr class="actual-data">
                                            <td>${response['name']}</td>
                                            <td>${response['height']}</td>
                                            <td>${response['mass']}</td>
                                            <td>${response['skin_color']}</td>
                                            <td>${response['hair_color']}</td>
                                            <td>${response['eye_color']}</td>
                                            <td>${response['birth_year']}</td>
                                            <td>${response['gender']}</td>
                                        </tr>`)
        }
    });
}


$('.voteButton').click(function(event){
    var clickedVoteButton = $(event.target)
    var planetId = clickedVoteButton.data('planetid').replace('ttps://swapi.co/api/planets/', '').slice(1, -1)
    var userId = clickedVoteButton.data('userid')
    var planetName = clickedVoteButton.data('planetname')
    console.log(planetId)
    transferVotePlanet(planetId, userId, planetName)
})


function transferVotePlanet(ptId, usrId, ptName){
    $.ajax({
      type: 'POST',
      url: '/vote',
      data: {'planetid': ptId,
             'userid': usrId,
             'planetname': ptName}
    })
    .done(function(completeHtmlPage) {
        location.reload()
   });
}
