import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { FormsModule } from '@angular/forms';
import { InterpretarService } from './services/interpretar.service';
import { C3DService } from './services/c3-d.service';
import { HttpClientModule } from '@angular/common/http';
import { MonacoEditorModule, MONACO_PATH } from '@materia-ui/ngx-monaco-editor';


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    MonacoEditorModule
  ],
   providers: [
    InterpretarService,
    C3DService,
    {
      provide: MONACO_PATH,
      useValue: 'https://unpkg.com/monaco-editor@0.19.3/min/vs'
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
