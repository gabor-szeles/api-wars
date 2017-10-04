//Paging event listeners and functions

$('#nextButton').click(function() {
    var nextPage = this.dataset.next;
    pager(nextPage);
});


$('#prevButton').click(function() {
    var prevPage = this.dataset.prev;
    pager(prevPage);
});


function pager(page) {
    $.ajax({
            type: 'POST',
            url: '/',
            data: {
                'next_page': page
            }
        })
        .done(function(completeHtmlPage) {
            $('body').empty();
            $('body').append(completeHtmlPage);
        });
}


//Residents Modal event listeners and functions

$('#residentsModal').on('show.bs.modal', function(event) {
    var clickedButton = $(event.relatedTarget); // Button that triggered the modal
    var planetName = clickedButton.data('planetname');
    var apiList = clickedButton.data('residentapilist');
    apiList = apiList.replace(/'/g, '').slice(1, -1).split(',');
    for (let api = 0; api < apiList.length; api++) {
        apiCall(apiList[api]);
    }
    $('.modal-title').text(`Known residents of ${planetName}`);
});


$('#residentsModal').on("hidden.bs.modal", function() {
    $('.actual-data').empty();
});


function apiCall(apiLink) {
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


//Voting event listener and function

$('.voteButton').click(function(event) {
    var clickedVoteButton = $(event.target);
    var planetId = clickedVoteButton.data('planetid').replace('ttps://swapi.co/api/planets/', '').slice(1, -1);
    var userId = clickedVoteButton.data('userid');
    var planetName = clickedVoteButton.data('planetname');
    transferVotePlanet(planetId, userId, planetName);
    clickedVoteButton.html('Voted!')
});


function transferVotePlanet(ptId, usrId, ptName) {
    $.ajax({
            type: 'POST',
            url: '/vote',
            data: {
                'planetid': ptId,
                'userid': usrId,
                'planetname': ptName
            }
        })
};


//Statistics modal event listeners

$('#statisticsModal').on('show.bs.modal', function() {
    $.ajax({
        dataType: 'json',
        url: '/get_vote_stats',
        success: function(response) {
            var statsData = response['stats']
            $('.statistics').append(`<tr>
                                        <th>Planet name</th>
                                        <th>Received votes</th>
                                    </tr>`)
            for (let obj = 0; obj < statsData.length; obj++) {
                let data = statsData[obj]
                $('.statistics').append(`<tr>
                                            <td id="planetName">${data['planet_name']}</td>
                                            <td id="planetVotes">${data['votes']}</td>
                                        </tr>`)
            }
        }
    });
});


$('#statisticsModal').on("hidden.bs.modal", function() {
    $('.statistics').empty()
});
