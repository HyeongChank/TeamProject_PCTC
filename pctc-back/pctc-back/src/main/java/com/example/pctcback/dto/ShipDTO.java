package com.example.pctcback.dto;

import lombok.*;

import java.util.Date;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
public class ShipDTO {

    private Integer progress;
    private int portorder;
    private String name;
    private String arrival;
    private String departure;
    private String unloading;
    private String loading ;
    private Date time;

}
