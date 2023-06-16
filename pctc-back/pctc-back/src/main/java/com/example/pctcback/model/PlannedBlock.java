package com.example.pctcback.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.Map;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
@ToString
@Getter
@Setter
public class PlannedBlock {
    @Id
    private String block;
    private Integer nowYard;
    private Integer nowShip;
    private Integer oneYard;
    private Integer oneShip;
    private Integer twoYard;
    private Integer twoShip;
    private Integer threeYard;
    private Integer threeShip;
    private Integer fourYard;
    private Integer fourShip;
    private Integer fiveYard;
    private Integer fiveShip;
}
