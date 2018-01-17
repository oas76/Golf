function saveplayer()
{
    console.log('Starting script');
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
                window.location = window.location.hostname + '/players'
            }
        }
    }

    req.open('POST', '/saveplayer')
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    var name = document.getElementById('newname').value
    var handicap = document.getElementById('newhandicap').value
    var postVars = 'newname='+name+'&'+'newhandicap='+handicap
    req.send(postVars)

    return false
}
