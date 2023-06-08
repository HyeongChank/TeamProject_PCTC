package com.example.pctcback.model;

import jakarta.persistence.*;
import lombok.*;
import java.util.Date;


@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Table(name = "YCOperation")
public class YardCraneOperation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String conNumber;
    private String opCode;
    private String shipCode;
    private Integer conYear;
    private String voyage;
    private String block;
    private Integer bay_x;
    private Integer row_y;
    private Integer tier_z;
    private String block2;
    private Integer bay_x2;
    private Integer row_y2;
    private Integer tier_z2;
    private String yardTruckNumber;
    private char fullOrEmpty; // 'F' for full, 'M' for empty
    private String containerSizeCode;
    private String equipmentNumber;
    private Date opCreationTime;
    private Date opCompletionTime;
    private Double opTime;

}
