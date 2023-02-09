nextflow.enable.dsl = 2nextflow

// params.pred = true
// params.loco = true
if([params.pred as Boolean, params.loco as Boolean].count(true) == 2){
    println "two are defined"
}

if([true, true].count(true) == 2){
    println "truth"
}

if(params.pred && params.loco){
    println "params are defined"
}


println "these are defined ${[params.pred, params.loco]}"

if([params.pred as Boolean, params.loco as Boolean].count(true) == 2){
    println "I'm true and creating channels"
} else if ([params.pred as Boolean, params.loco as Boolean].count(true) == 1) {
    exit 1, "Both '--pred' and '--loco' need to be defined at the same time"
} else {
    println "I'm runnning step1"
}

ch = Channel.from( 1, 3, 5, 7 )
if (params.pred){
    process foo {
        process_var = 42
        def other_var = 42
        cpus = 2

        input:
        val(meta) from ch_meta_input
        file(test1) from ch_test1_input
        set file(test1), file(${test2}) from ch_set_input

        output:
        set (file_output) into foo_output

        exec:
        id = meta.id
        def local_var = 1
    }
}

if (!params.a) {
    if (params.gf == 'vcf') {
        process vcf {

        }
    }
    else if (params.gf == 'bgen') {
        process bgen {

        }
    }
    else if (params.gf == 'pgen') {
        process pgen {

        }
    }
    else if (params.gf == 'plink') {
        process bfile {

        }
    }
    else if (params.gf == 'dosage') {
        process dosage {

        }
    }
}

process bar_eret {}

process bar {                                                                   
    barist = 42                                                            
                                                                      
    input:                                                                      
    val(meta)

    exec:                                                                       
    id = meta.id                                                                
    def local_var = 1                                                           
                                   
}

workflow sub_foo_bar {
    take:
    input1
    input2

    main:
    foo(input1)
    bar(input2)
}

workflow {                                                                      
    //foo([id: "test"])
    //bar([id: "barrr"])
    sub_foo_bar([id: "test"],[id: "barrr"])
}
//if(\s+)?\(\S+\)\{\n(\s+)?process...
//(\s+)?if(\s+)?\(.*\)(\s+)\{(.*?)\n(\s+)?\}
//process\s+(\w+)\s+\{(.*?)\n(\s+)?\}