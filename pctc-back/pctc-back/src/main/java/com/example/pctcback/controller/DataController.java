package com.example.pctcback.controller;

import com.example.pctcback.dto.DataDTO;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.client.RestTemplate;

@RequestMapping("/api")
public class DataController {
    @PostMapping ("/congestion")
    public ResponseEntity<?> PythonResponse(@RequestBody DataDTO dto){
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        String jsonBody = "{\"new_value\": 1300, \"new_termCode\": \"BNCT\"}";
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(jsonBody,headers);
        String url = "http://10.125.121.220:5001/api/congestion";
        String response =restTemplate.postForObject(url, entity, String.class);
        return ResponseEntity.ok(response);
    }
}
