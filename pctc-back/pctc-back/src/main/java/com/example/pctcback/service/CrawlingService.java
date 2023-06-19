package com.example.pctcback.service;

import com.example.pctcback.model.BerthStatus;
import com.example.pctcback.model.PlannedBlock;
import com.example.pctcback.model.Ship;
import com.example.pctcback.persistence.BerthStatusRepository;
import com.example.pctcback.persistence.PlannedBlockRepository;
import com.example.pctcback.persistence.ShipRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStreamReader;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

@Service
public class CrawlingService {
    private final ShipRepository shipRepository;
    private final BerthStatusRepository berthStatusRepository;
    private final PlannedBlockRepository plannedBlockRepository;
    @Autowired
    public CrawlingService(ShipRepository shipRepository, BerthStatusRepository berthStatusRepository, PlannedBlockRepository plannedBlockRepository) {
        this.shipRepository = shipRepository;
        this.berthStatusRepository = berthStatusRepository;
        this.plannedBlockRepository = plannedBlockRepository;
    }
    private WebDriver settingWebDriver(String address){
        ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.addArguments("--remote-allow-origins=*");    // 해당 부분 추가
        System.setProperty("webdriver.chrome.driver", "C:/Users/SW/Desktop/chromedriver/chromedriver.exe");
        WebDriver driver = new ChromeDriver(chromeOptions);
        driver.get(address);
        return driver;

    }


//    @Scheduled(fixedRate = 600000)
    public void runScrapyScript(){
        System.out.println("Scrapy is Starting..."); // 추후에 뺴서 둘것.
        ProcessBuilder processBuilder = new ProcessBuilder("scrapy","runspider","D:/SDH/TeamProject/TeamProject_PCTC/pctc-back/pctc-back/src/main/resources/Scrapsite.py");
        try{
            Process process = processBuilder.start();
            InputStreamReader reader = new InputStreamReader(process.getInputStream());
            StringBuilder output = new StringBuilder();
            int ch;
            while ((ch = reader.read()) != -1) {
                output.append((char) ch);

            }
            String jsonString = output.toString();
            ObjectMapper mapper = new ObjectMapper();
            List<Ship> shipList = mapper.readValue(jsonString,mapper.getTypeFactory().constructCollectionType(List.class,Ship.class));
            shipRepository.deleteAll();
            shipRepository.saveAll(shipList);
        }catch (IOException e){
            e.printStackTrace();
        }

    }
    public List<Ship> PortStatus(){
        return shipRepository.findAll();
    }
//    @Transactional
//    @Scheduled(fixedRate = 650000)
    public void berthStatus() {
        WebDriver driver = settingWebDriver("http://info.bptc.co.kr:9084/content/sw/frame/berth_status_text_frame_sw_kr.jsp?p_id=BETX_SH_KR&snb_num=2&snb_div=service");
        WebElement month = driver.findElement(By.cssSelector("#container > section > section > section > form > table > thead > tr:nth-child(1) > td:nth-child(2) > label:nth-child(3) > input[type=radio]"));
        month.click();
        WebElement ele = driver.findElement(By.cssSelector("#container > section > section > section > form > table > thead > tr:nth-child(1) > td.tCenter > span > input[type=submit]"));
        ele.click();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofMillis(100L));
        driver.switchTo().frame("output");
        WebElement loading = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("body > p")));
        List<WebElement> elements = driver.findElements(By.cssSelector(".tabletypeC tbody tr td"));
        BerthStatus bbb = null;
        berthStatusRepository.deleteAll();
        for (int i = 15; i<= elements.size() ; i+=15){
                bbb = BerthStatus.builder()
                        .shipOrder(elements.get(i - 15).getText())
                        .Vessel(elements.get(i - 14).getText())
                        .shipName(elements.get(i - 13).getText())
                        .berthing(elements.get(i - 12).getText())
                        .shipOwner(elements.get(i - 11).getText())
                        .scheduledArrivalTime(elements.get(i - 10).getText())
                        .arrivalTime(elements.get(i - 9).getText())
                        .workTime(elements.get(i - 8).getText())
                        .departureTime(elements.get(i - 7).getText())
                        .cargoTime(elements.get(i - 6).getText())
                        .discharge(parseInt(elements.get(i - 5).getText()))
                        .loading(parseInt(elements.get(i - 4).getText()))
                        .shifting(parseInt(elements.get(i - 3).getText()))
                        .transship(elements.get(i - 2).getText())
                        .route(elements.get(i-1).getText())
                        .build();
                berthStatusRepository.save(bbb);

        }
        driver.quit();
    }
//    @Scheduled(fixedRate = 650000)
    public List<Map<String,Map<String,Integer>>> emptyContainer() {
        WebDriver driver = settingWebDriver("http://info.bptc.co.kr:9084/content/od/frame/yard_empty_frame_od_kr.jsp?p_id=EMPT_ON_KR&snb_num=8&snb_div=service&pop_ok=Y");
        List<WebElement> listcon = driver.findElements(By.cssSelector("#container > section > section > section > table > tbody:nth-child(4) > tr> td"));
        List<Map<String, Map<String, Integer>>> results = new ArrayList<>();
        for (int i = 20; i <= listcon.size(); i += 20) {
                String key = listcon.get(i-20).getText();
                Map<String, Integer> values = new HashMap<>();
                values.put("PL20", parseInt(listcon.get(i-19).getText()));
                values.put("PL40", parseInt(listcon.get(i-18).getText()));
                values.put("PL45", parseInt(listcon.get(i-17).getText()));
                values.put("GP20", parseInt(listcon.get(i-16).getText()));
                values.put("GP40", parseInt(listcon.get(i-15).getText()));
                values.put("GP45", parseInt(listcon.get(i-14).getText()));
                values.put("OT20", parseInt(listcon.get(i-13).getText()));
                values.put("OT40", parseInt(listcon.get(i-12).getText()));
                values.put("OT45", parseInt(listcon.get(i-11).getText()));
                values.put("FL20", parseInt(listcon.get(i-10).getText()));
                values.put("FL40", parseInt(listcon.get(i-9).getText()));
                values.put("FL45", parseInt(listcon.get(i-8).getText()));
                values.put("HQ20", parseInt(listcon.get(i-7).getText()));
                values.put("HQ40", parseInt(listcon.get(i-6).getText()));
                values.put("HQ45", parseInt(listcon.get(i-5).getText()));
                values.put("DC20", parseInt(listcon.get(i-4).getText()));
                values.put("DC40", parseInt(listcon.get(i-3).getText()));
                values.put("DC45", parseInt(listcon.get(i-2).getText()));
                values.put("total",parseInt(listcon.get(i-1).getText()));
                Map<String, Map<String,Integer>> result = new HashMap<>();
                result.put(key, values);
                results.add(result);


        }
        driver.quit();
        System.out.println("results = " + results);
        return results;


    }
    @Scheduled(fixedRate = 1024000)
    public void scheduledContainerOperation() throws InterruptedException {
//        WebDriver driver = settingWebDriver("https://info.bptc.co.kr/content/YardState1.jsp?gu=0");
//        List<WebElement> elements =driver.findElements(By.cssSelector("body > table > tbody > tr > td > table > tbody > tr > td"));
//        for (WebElement element : elements) {
//            System.out.println(element.getText());
//        }
//        driver = settingWebDriver("https://info.bptc.co.kr/content/YardState1.jsp?gu=1");
//        List<WebElement> elements1 =driver.findElements(By.cssSelector("body > table > tbody > tr > td > table > tbody > tr > td"));
//        for (WebElement element : elements1) {
//            elements.add(element);
//            System.out.println(element.getText());
//        }
//
//        driver = settingWebDriver("https://info.bptc.co.kr/content/YardState1.jsp?gu=2");
//        List<WebElement> elements2 =driver.findElements(By.cssSelector("body > table > tbody > tr > td > table > tbody > tr > td"));
//        for (WebElement element : elements2) {
//            elements.add(element);
//            System.out.println(element.getText());
//        }
//
//        driver = settingWebDriver("https://info.bptc.co.kr/content/YardState1.jsp?gu=3");
//        List<WebElement> elements3 =driver.findElements(By.cssSelector("body > table > tbody > tr > td > table > tbody > tr > td"));
//        for (WebElement element : elements3) {
//            elements.add(element);
//            System.out.println(element.getText());
//        }
        List<String> urls = List.of(
                "https://info.bptc.co.kr/content/YardState1.jsp?gu=0",
                "https://info.bptc.co.kr/content/YardState1.jsp?gu=1",
                "https://info.bptc.co.kr/content/YardState1.jsp?gu=2",
                "https://info.bptc.co.kr/content/YardState1.jsp?gu=3"
        );
        List<WebElement> elements = new ArrayList<>();
        ExecutorService executor = Executors.newFixedThreadPool(urls.size());
        for (String url : urls) {
            executor.execute(() -> {
                WebDriver driver = settingWebDriver(url);
                List<WebElement> pageElements = driver.findElements(By.cssSelector("body > table > tbody > tr > td > table > tbody > tr > td"));

                synchronized (elements) {
                    elements.addAll(pageElements);
                }
                for (int i = 13; i <= elements.size(); i += 13) {
                    PlannedBlock plannedBlock = PlannedBlock.builder()
                            .block(elements.get(i-13).getText())
                            .nowYard(parseInt(elements.get(i-12).getText()))
                            .nowShip(parseInt(elements.get(i-11).getText()))
                            .oneYard(parseInt(elements.get(i-10).getText()))
                            .oneShip(parseInt(elements.get(i-9).getText()))
                            .twoYard(parseInt(elements.get(i-8).getText()))
                            .twoShip(parseInt(elements.get(i-7).getText()))
                            .threeYard(parseInt(elements.get(i-6).getText()))
                            .threeShip(parseInt(elements.get(i-5).getText()))
                            .fourYard(parseInt(elements.get(i-4).getText()))
                            .fourShip(parseInt(elements.get(i-3).getText()))
                            .fiveYard(parseInt(elements.get(i-2).getText()))
                            .fiveShip(parseInt(elements.get(i-1).getText()))
                            .build();

                    updatePlannedBlock(plannedBlock);
                    System.out.println("plannedBlock.toString() = " + plannedBlock.toString());
                }
                driver.quit();
                executor.shutdown();
            });
        }
        boolean awaitTermination = executor.awaitTermination(Long.MAX_VALUE, TimeUnit.MILLISECONDS);
        if (awaitTermination) {
            executor.shutdown();
        } else {
            System.out.println(" Thread error occured");
        }



    }
    public synchronized void updatePlannedBlock(PlannedBlock plannedBlock) {
        // ID 값이 같은 데이터가 이미 존재하는지 확인
        Optional<PlannedBlock> existingBlock = plannedBlockRepository.findById(plannedBlock.getBlock());
        if (existingBlock.isPresent()) {
            // ID 값이 같은 데이터가 이미 존재하면 UPDATE 구문 실행
            PlannedBlock updatedBlock = existingBlock.get();
            updatedBlock.setNowYard(updatedBlock.getNowYard() + plannedBlock.getNowYard());
            updatedBlock.setNowShip(updatedBlock.getNowShip() + plannedBlock.getNowShip());
            updatedBlock.setOneYard(updatedBlock.getOneYard() + plannedBlock.getOneYard());
            updatedBlock.setOneShip(updatedBlock.getOneShip() + plannedBlock.getOneShip());
            updatedBlock.setTwoYard(updatedBlock.getTwoYard() + plannedBlock.getTwoYard());
            updatedBlock.setTwoShip(updatedBlock.getTwoShip() + plannedBlock.getTwoShip());
            updatedBlock.setThreeYard(updatedBlock.getThreeYard() + plannedBlock.getThreeYard());
            updatedBlock.setThreeShip(updatedBlock.getThreeShip() + plannedBlock.getThreeShip());
            updatedBlock.setFourYard(updatedBlock.getFourYard() + plannedBlock.getFourYard());
            updatedBlock.setFourShip(updatedBlock.getFourShip() + plannedBlock.getFourShip());
            updatedBlock.setFiveYard(updatedBlock.getFiveYard() + plannedBlock.getFiveYard());
            updatedBlock.setFiveShip(updatedBlock.getFiveShip() + plannedBlock.getFiveShip());

            plannedBlockRepository.save(updatedBlock);

        } else {
            // ID 값이 같은 데이터가 없으면 INSERT 구문 실행
            plannedBlockRepository.save(plannedBlock);
        }
    }


    private Integer parseInt(String value){
        if(value.isEmpty()){
            return 0;
        }else if(value.trim().isEmpty()){
            return 0;
        }else{
            return Integer.parseInt(value);
        }

    }

}
