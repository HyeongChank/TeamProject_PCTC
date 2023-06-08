package com.example.pctcback.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.Date;

@Entity
@Getter
@Table(name = "Shipprogress")
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Ship {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Integer progress;
    private int portorder;
    private String name;
    private String arrival;
    private String departure;
    private String unloading;
    private String loading ;
    @Temporal(TemporalType.TIMESTAMP)
    private final Date time = new Date();

}
