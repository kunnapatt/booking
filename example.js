require('chromedriver') ;

var webdriver = require('selenium-webdriver') ;
var By = webdriver.By ;
var until = webdriver.until ;

var driver = new webdriver.Builder()
    .forBrowser('chrome')
    .build() ;

function test(){
    return new Promise((resolve, reject) => {
        driver.get('http://www.google.com/ncr');
        driver.findElement(By.className("gLFyf gsfi")).sendKeys("Test na kubb") ;
        driver.findElement(By.className('gNO89b')).click() ;
        resolve() ;
    })
}

var myvar = test() ;
myvar.then(() => {console.log("Promise Accepted")})
    .catch(() => {console.log("Promise Rejected")})

// driver.wait(until.titleIs('Test na kubb - Google Search'), 5000);
