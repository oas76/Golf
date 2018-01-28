function loadXMLDoc()
{
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if (req.readyState == 4)
        {
            if (req.status != 200)
            {
                    //error handling code here
            }
            else
            {
                var response = JSON.parse(req.responseText);
                if(response.tournament)
                {
                    var temp = '<ul class="list-group"> {{#pairings}} <li class="list-group-item">{{players}} <span class="badge"> {{hc}} </span> </li> {{/pairings}} </ul>';
                    html = Mustache.to_html(temp, response.tournament);
                    document.getElementById('myDiv').innerHTML = html;
                }
                else
                {
                    document.getElementById('myDiv').innerHTML = "Invalid Teamsize"
                }


            }
        }
    }

    req.open('POST', '/randomize')
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    var teamsize = document.getElementById('teamsize').value
    var postVars = 'teamsize='+teamsize
    req.send(postVars)

    return false
}
