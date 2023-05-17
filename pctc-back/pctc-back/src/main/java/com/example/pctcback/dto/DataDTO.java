package com.example.pctcback.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Data
public class DataDTO {
    private int num;
    private String wtTime;
    private String congestLevel;

}