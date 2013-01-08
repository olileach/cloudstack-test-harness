$(function() {
    $('#results-detail td').each(function() {
        if ($(this).html() == "1" && $(this).next().html() == "None") {
            $(this).next().html("in progress");
        }
    });
});


$(function() {
     $('#results-detail td').each(function() {
         var html = $(this).html();
         $(this).html(
             html.replace(/0/,'<b>no</b>')
                 .replace(/1/,'<b>yes</b>')
                 .replace(/2/,'<b>completed</b>')
                 .replace(/in progress/g, "<img id=throbber src=/static/images/throbber.gif </img> ")
                 .replace(/failed/g, "<span style=\"color: red; font-weight: bold\">failed</span>")
                 .replace(/success/g, "<span style=\"color: green; font-weight: bold;\">success</span>")
                 .replace(/completed/g, "<span style=\"color: Gray18; font-weight: bold;\">completed</span>")
                 .replace(/None/g, "<b></b>")
         );
     });
});



// refreshes page - used instead of AJAX

window.onload = setupRefresh;

function setupRefresh() {
    setTimeout("refreshPage();", 30000); // milliseconds
    }

function refreshPage() {
    window.location = location.href;
    }

// end of refreh page code


// table zebra settings
//
$(document).ready(function(){
    $("#results-detail tr:odd").addClass("odd");
    $("#results-detail tr:even").addClass("even");
});
