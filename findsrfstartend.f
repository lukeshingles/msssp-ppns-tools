	program findsrfstartend
	implicit none

* evolution files 
        CHARACTER ifilename*60
        REAL*8  M,T
        integer i, j, pulse(500), npulse
	integer nmod(500)

        real output(500,6)	
	real mtot(500), mcore(500), menv(500)
        real lum(500), per(500)

* srffiles
	character filein*60
	integer nevmlast, iflag, nev, nevm0, nsurf
	integer model(200000)
	real*8 temp(400), abund(200000,400), evage
* output
	character ele(400)*2
	integer k, ncount, ne
	integer keep, keepmod
	integer ife, io
	integer tpnumb

*s
* READ surf files
*
        open(unit=10,file='srffiles.list',form='formatted')
        iflag = 0
 400    continue
        nevmlast=-1
	j=0
        read(10,105,end=205) filein 
        write(6,*) filein
 105    format(a)
        open(unit=11,file=filein,form='formatted')
 102    continue
        read(11,*,end=300) nev,nevm0,evage, (temp(i),i=1,nev)
        if (nevm0.le.nevmlast) then
		go to 102
	end if
        j=j+1
	if (j==1) write(6,'(A16,I10)')'   evmod first:',nevm0
        nevmlast=nevm0
        go to 102
 300    continue                !No more models in this file: open next file
	write(6,'(A16,I10)') '   evmod last: ',nevm0
        write(6,*) 'number of models:',j
        go to 400
 205    continue                !No more files to be processed
        nsurf=j

	stop
	END


