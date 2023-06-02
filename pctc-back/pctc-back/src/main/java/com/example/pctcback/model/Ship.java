package com.example.pctcback.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Table(name = "ShipProgress")
public class Ship {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String conNumber;
    private String containerSizeCode;
    private String containerTypeCode;
    private String shipCode;
    private int yearCol;
    private String voyage;
    private double weight;
    private String destinationPort;
    private String shippingPort;
    private Date time;

}
