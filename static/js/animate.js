    var i=0;
    var j=0;
    var text = "Greetings Folks".split('');
    var shop = "Let's Go Shopping".split('')
    function typing(){
        if(i<text.length){
            document.getElementById("welcome").innerHTML+=text[i];
            i++;
            setTimeout(typing,100);
        }
    }
    function typing2(){
        if(j < shop.length){
            document.getElementById("welcome").innerHTML+=shop[j];
            j++;
            setTimeout(typing2,100);
        }
    }
    function fade(){
        $("#welcome").animate({
            opacity: '0'
            }, "slow");
    }
    function transition(){
        $("#title_sec").animate({
            height: '0px'
            });
    }
    function show(){
        document.getElementById('welcome').innerHTML = "";
        document.getElementById('welcome').style.opacity = 1;
    }
    
