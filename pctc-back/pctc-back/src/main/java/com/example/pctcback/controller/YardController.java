package com.example.pctcback.controller;

import com.example.pctcback.service.ScrapyService;
import com.example.pctcback.service.YCOService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

@RestController
public class YardController {
    @Autowired
    YCOService ycoservice;
    @Autowired
    ScrapyService scrapyService;
    @GetMapping("/yard")
    public ResponseEntity<?> YardStatusController(){
        String blockstr =  "1A,1B,1C,1D,1E,1F,1G,1H,1I," +
                "2A,2B,2C,2D,2E,2F,2G,2H,2I," +
                "3A,3B,3C,3D,3E,3F,3G,3H,3I,3J,3K," +
                "4A,4B,4C,4D,4E,4F,4G,4H,4I," +
                "5A,5B,5C,5D,5E,5F,5G,5H," +
                "6A,6B,6C,6D,6E,6F," +
                "7A,7B,7C,7D,7E,7F,7G," +
                "8A,8B,8C,8D,8E,8F,8G," +
                "9A,9B,9C,9D,9E,9F,9G";
        String[] blockarray = blockstr.split(",");
        List<String> blocks = Arrays.asList(blockarray);
        Map<String, Integer> block_number =  ycoservice.ConNumBlock(blocks);
        return ResponseEntity.ok().body(block_number);
    }

    @GetMapping("/")
    public String YardInit(){
        ycoservice.myMethod("D:/SDH/TeamProject/TeamProject_PCTC/pctc-back/pctc-back/data/YardStatus.csv");
        return "현재 DB 에 정보 넣는중";
    }
    @GetMapping("/port")
    public ResponseEntity<?> PortStatusController(){


        return ResponseEntity.ok().body(scrapyService.PortStatus());

    }



}
