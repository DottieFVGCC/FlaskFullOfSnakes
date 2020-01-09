// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  console.log("hello world :o");
  //load starting list of comments when page loads
  $.get("/comments", function(comments) {
    comments.forEach(function(comment) {
      $("<li></li>")
        .text(comment)
        .appendTo("ul#comments");
    });
  });
  
  $.get("/leaderboard", function(leaders) {
    leaders.forEach(function(leader) {
      $("<li></li>")
        .text(leader)
        .appendTo("ul#leaders");
    });
  });

  //add a comment to the list by posting to the server for 
  // storage in the data list and updating the html list on client
  $("#formComment").submit(function(event) {
    event.preventDefault();
    var newComment = $("#newComment").val();
    alert(newComment);
    $.post("/comments?" + $.param({ comment: newComment }), function() {
      $("<li></li>")
        .text(newComment)
        .appendTo("ul#comments");
      $("#newComment").val("");
      $("#newComment").focus();
    });
  });

  // get the current player's name, store on server, and display on client
  $("#formUser").submit(function(event) {
    event.preventDefault();
    var user = $("#userName").val();      
    var score = $("#score").text();
         
    //Pass object as parameter; server will interpret as form data
    $.post("/user", { user: user, score: score}, function(data) {
      alert(data); 
       $("<li></li>")
        .text(user + ": " + score)
        .appendTo("ul#leaders");
    });   
  });
});
