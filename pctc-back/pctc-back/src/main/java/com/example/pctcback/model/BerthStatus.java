package com.example.pctcback.model;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
@Entity
@Getter
@Table(name = "BerthStatus")
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class BerthStatus {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private String shipOrder;
    private String Vessel;
    private String shipName;
    private String berthing;
    private String shipOwner;
    private String scheduledArrivalTime;
    private String arrivalTime;
    private String workTime;
    private String departureTime;
    private String cargoTime;
    private Integer discharge;
    private Integer loading;
    private Integer shifting;
    private String transship;
    private String route;
}

