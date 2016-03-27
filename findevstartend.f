      program selectp

      CHARACTER RESP*1, IFILENAME*60,DIR*30,DIRECT*30,OFILENAME*60
     $     ,IFILE2*60
      DOUBLE PRECISION TIMEFIRST,TIMELAST,MASS1,MASS2
      REAL OUTPUT(62)

 10   print 241
 241  FORMAT(/,' INPUT FILE:   Enter ev filename > ',$,A1)
      read 342,IFILENAME
 342  FORMAT(A30)
 
      open(unit=10,name=ifilename,form='unformatted',type='old')
     
 973  READ(10) MASS1 
      WRITE(*,*) 'Mass:       ',MASS1
      READ(10) NMODELFIRST,TIMEFIRST,(OUTPUT(I),I=1,62)
 100  READ(10,END=200) NMODELLAST,TIMELAST,(OUTPUT(I),I=1,62)
      !WRITE(*,*)NMODELLAST,TIMELAST
      GO TO 100

 200  continue

      write(*,*)'First model:',NMODELFIRST,',  T=',TIMEFIRST
      write(*,*)'Last model: ',NMODELLAST, ',  T=',TIMELAST

      close(10)
      close(30)
      STOP
      END
