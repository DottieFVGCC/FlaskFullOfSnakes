// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  console.log("hello world :o");

  $.get("/comments", function(comments) {
    comments.forEach(function(comment) {
      $("<li></li>")
        .text(comment)
        .appendTo("ul#comments");
    });
  });

  $("#formComment").submit(function(event) {
    event.preventDefault();
    var newComment = $("#newComment").val();
    alert(newComment);
    $.post("/comments?" + $.param({ comment: newComment }), function() {
      $("<li></li>")
        .text(newComment)
        .appendTo("ul#comments");
      $("input").val("");
      $("input").focus();
    });
  });

  $("#formUser").submit(function(event) {
    event.preventDefault();
    var user = $("#userName").val();
    $.post("/user?" + $.param({ user: user }), function(data) {
      alert(data);
    });
  });
});
